import csv
import json

from libertydiff.diff import compare_paths, summary_text, write_csv, write_json


BASE = '''library (demo) {
  time_unit : "1ns";
  capacitive_load_unit (1,pf);
  lu_table_template ("delay") {
    variable_1 : input_net_transition;
    variable_2 : total_output_net_capacitance;
  }
  lu_table_template ("delay_rev") {
    variable_1 : total_output_net_capacitance;
    variable_2 : input_net_transition;
  }
  cell (inv) { pin (Y) { timing () {
    related_pin : "A";
    cell_rise ("delay") {
      index_1 ("0.1, 0.2");
      index_2 ("0.01, 0.02");
      values ("1, 2", "3, 4");
    }
  } } }
}
'''


def test_identity(tmp_path):
    path = tmp_path / "a.lib"
    path.write_text(BASE)
    comparison = compare_paths(path, path)
    assert len(comparison.differences) == 4
    assert all(point.absolute_difference_ps == 0 for point in comparison.differences)
    assert all(point.percentage_difference == 0 for point in comparison.differences)


def test_exact_ten_percent_change(tmp_path):
    a = tmp_path / "a.lib"
    b = tmp_path / "b.lib"
    a.write_text(BASE.replace('"1, 2", "3, 4"', '"1.1, 2", "3, 4"'))
    b.write_text(BASE)
    comparison = compare_paths(a, b)
    changed = [point for point in comparison.differences if point.absolute_difference_ps != 0]
    assert len(changed) == 1
    assert changed[0].percentage_difference == 10
    assert changed[0].absolute_difference_ps == 100


def test_axes_swapped_and_values_transposed(tmp_path):
    a = tmp_path / "a.lib"
    b = tmp_path / "b.lib"
    a.write_text(BASE)
    b.write_text(BASE.replace('cell_rise ("delay")', 'cell_rise ("delay_rev")')
                    .replace('index_1 ("0.1, 0.2")', 'index_1 ("0.01, 0.02")')
                    .replace('index_2 ("0.01, 0.02")', 'index_2 ("0.1, 0.2")')
                    .replace('values ("1, 2", "3, 4")', 'values ("1, 3", "2, 4")'))
    comparison = compare_paths(a, b)
    assert len(comparison.differences) == 4
    assert all(point.absolute_difference_ps == 0 for point in comparison.differences)


def test_unmatched_and_outputs(tmp_path):
    a = tmp_path / "a.lib"
    b = tmp_path / "b.lib"
    a.write_text(BASE)
    b.write_text(BASE.replace('cell (inv)', 'cell (other)'))
    comparison = compare_paths(a, b)
    assert not comparison.differences
    assert sum(item.points for item in comparison.unmatched) == 8
    assert "unmatched 8 points" in summary_text(comparison)
    csv_path = tmp_path / "out.csv"
    json_path = tmp_path / "out.json"
    write_csv(comparison, csv_path)
    write_json(comparison, json_path)
    assert list(csv.DictReader(csv_path.open())) == []
    payload = json.loads(json_path.read_text())
    assert payload["points_unmatched"] == 8
    assert len(payload["unmatched"]) == 2
