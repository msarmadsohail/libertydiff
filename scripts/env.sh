_cellchar_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
_cellchar_repo_root="$(cd -- "$_cellchar_script_dir/.." && pwd)"
export PATH="$_cellchar_repo_root/.tools/envs/ngspice/Library/bin:$PATH"
export PDK_ROOT="$_cellchar_repo_root/pdk/ciel/sky130/versions/e7a6777d157a9d94c7ac757457b9e4309e9e9000"
export PDK=sky130A
unset _cellchar_script_dir _cellchar_repo_root
