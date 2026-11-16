from pathlib import Path

from libertydiff.reader import read_library


HEADER = '''library (demo) {
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
  lu_table_template ("scalar") { }
'''


def write(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "demo.lib"
    path.write_text(HEADER + body + "\n}\n")
    return path


def test_input_first_and_multiline_values(tmp_path):
    path = write(tmp_path, '''
  cell (inv) { pin (Y) { timing () {
    related_pin : "A";
    cell_rise ("delay") {
      index_1 ("0.1, 0.2");
      index_2 ("0.01, 0.02");
      values ( \\
        "1, 2", \\
        "3, 4" \\
      );
    }
  } } }
''')
    table = read_library(path).tables[0]
    assert [axis.name for axis in table.axes] == ["input_net_transition", "total_output_net_capacitance"]
    assert table.values == (1, 2, 3, 4)
    assert table.units.time_ps == 1000
    assert table.units.capacitance_ff == 1000


def test_load_first_is_preserved_with_variable_names(tmp_path):
    path = write(tmp_path, '''
  cell (inv) { pin (Y) { timing () {
    related_pin : "A";
    cell_fall ("delay_rev") {
      index_1 ("0.01, 0.02");
      index_2 ("0.1, 0.2");
      values ("1, 2", "3, 4");
    }
  } } }
''')
    table = read_library(path).tables[0]
    assert [axis.name for axis in table.axes] == ["total_output_net_capacitance", "input_net_transition"]
    assert table.axes[0].values == (0.01, 0.02)
    assert table.values == (1, 2, 3, 4)


def test_scalar_table(tmp_path):
    path = write(tmp_path, '''
  cell (inv) { pin (Y) { timing () {
    related_pin : "A";
    cell_rise ("scalar") { values ("0.125"); }
  } } }
''')
    table = read_library(path).tables[0]
    assert table.axes == ()
    assert table.values == (0.125,)


def test_picosecond_header_units(tmp_path):
    path = tmp_path / "units.lib"
    path.write_text('''library (units) {
      time_unit : "1ps";
      capacitive_load_unit (1,ff);
      cell (inv) { pin (Y) { timing () { related_pin : "A";
        cell_rise ("scalar") { values ("12"); }
      } } }
    }''')
    assert read_library(path).units.time_ps == 1
    assert read_library(path).units.capacitance_ff == 1
