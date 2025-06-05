
## Recent Findings

```
 rezv6y-codex/revamp-documentation-and-contribution-guide
=======
 codex/improve-fundalyze-ui/ux

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_e2e.py ______________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_e2e.py:4: in <module>
    import modules.generate_report.report_generator as rg
modules/generate_report/__init__.py:3: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 58
E       codex/audit-and-remediate-bugs-in-codebase
E                                                 ^
E   IndentationError: unindent does not match any outer indentation level
________________ ERROR collecting tests/test_excel_dashboard.py ________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_excel_dashboard.py:3: in <module>
    from generate_report.excel_dashboard import (
modules/generate_report/__init__.py:3: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 58
E       codex/audit-and-remediate-bugs-in-codebase
E                                                 ^
E   IndentationError: unindent does not match any outer indentation level
_____________ ERROR collecting tests/test_excel_dashboard_extra.py _____________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_excel_dashboard_extra.py:3: in <module>
    from modules.generate_report.excel_dashboard import (
modules/generate_report/__init__.py:3: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 58
E       codex/audit-and-remediate-bugs-in-codebase
E                                                 ^
E   IndentationError: unindent does not match any outer indentation level
_________________ ERROR collecting tests/test_fallback_data.py _________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_fallback_data.py:5: in <module>
    import modules.generate_report.fallback_data as fb
modules/generate_report/__init__.py:3: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 58
E       codex/audit-and-remediate-bugs-in-codebase
E                                                 ^
E   IndentationError: unindent does not match any outer indentation level
_______________ ERROR collecting tests/test_metadata_checker.py ________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_metadata_checker.py:5: in <module>
    import modules.generate_report.metadata_checker as mc
modules/generate_report/__init__.py:3: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 58
E       codex/audit-and-remediate-bugs-in-codebase
E                                                 ^
E   IndentationError: unindent does not match any outer indentation level
________________ ERROR collecting tests/test_output_dir_env.py _________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_output_dir_env.py:3: in <module>
    import modules.generate_report.report_generator as rg
modules/generate_report/__init__.py:3: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 58
E       codex/audit-and-remediate-bugs-in-codebase
E                                                 ^
E   IndentationError: unindent does not match any outer indentation level
=========================== short test summary info ============================
ERROR tests/test_e2e.py
ERROR tests/test_excel_dashboard.py
ERROR tests/test_excel_dashboard_extra.py
ERROR tests/test_fallback_data.py
ERROR tests/test_metadata_checker.py
ERROR tests/test_output_dir_env.py
!!!!!!!!!!!!!!!!!!! Interrupted: 6 errors during collection !!!!!!!!!!!!!!!!!!!!
6 errors in 2.85s
=======
 main
........................................................................ [ 61%]
..............................................                           [100%]
=============================== warnings summary ===============================
tests/test_portfolio_manager.py::test_add_new_ticker_with_nas_present
tests/test_portfolio_manager.py::test_add_ticker_to_all_na_column
  /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py:268: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
    portfolio = pd.concat([portfolio, new_row], ignore_index=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
 rezv6y-codex/revamp-documentation-and-contribution-guide
118 passed, 2 warnings in 14.74s
=======
118 passed, 2 warnings in 18.89s

> main
```

## Recent Findings

```
........................................................................ [ 61%]
..............................................                           [100%]
=============================== warnings summary ===============================
tests/test_portfolio_manager.py::test_add_new_ticker_with_nas_present
tests/test_portfolio_manager.py::test_add_ticker_to_all_na_column
 rezv6y-codex/revamp-documentation-and-contribution-guide
=======
 codex/improve-fundalyze-ui/ux
  /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py:273: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
    portfolio = pd.concat([portfolio, new_row], ignore_index=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
118 passed, 2 warnings in 12.49s
=======
 main
  /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py:268: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
    portfolio = pd.concat([portfolio, new_row], ignore_index=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
 rezv6y-codex/revamp-documentation-and-contribution-guide
118 passed, 2 warnings in 14.93s
=======
118 passed, 2 warnings in 19.60s
main
 main
```

## 🧪 Pytest Results
```

==================================== ERRORS ====================================
______________ ERROR collecting tests/test_directus_tools_init.py ______________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_directus_tools_init.py:4: in <module>
    from modules.management.directus_tools import run_directus_wizard
modules/management/__init__.py:3: in <module>
    from .portfolio_manager.portfolio_manager import main as run_portfolio_manager
E     File "/workspace/Fundalyze/modules/management/portfolio_manager/__init__.py", line 1
E       codex/create-comprehensive-documentation-for-fundalyze
E   IndentationError: unexpected indent
______________________ ERROR collecting tests/test_e2e.py ______________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_e2e.py:5: in <module>
    import modules.generate_report.report_generator as rg
modules/generate_report/__init__.py:12: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 77
E       codex/create-comprehensive-documentation-for-fundalyze
E                                                             ^
E   IndentationError: unindent does not match any outer indentation level
________________ ERROR collecting tests/test_excel_dashboard.py ________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_excel_dashboard.py:4: in <module>
    from generate_report.excel_dashboard import (
modules/generate_report/__init__.py:12: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 77
E       codex/create-comprehensive-documentation-for-fundalyze
E                                                             ^
E   IndentationError: unindent does not match any outer indentation level
_____________ ERROR collecting tests/test_excel_dashboard_extra.py _____________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_excel_dashboard_extra.py:4: in <module>
    from modules.generate_report.excel_dashboard import (
modules/generate_report/__init__.py:12: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 77
E       codex/create-comprehensive-documentation-for-fundalyze
E                                                             ^
E   IndentationError: unindent does not match any outer indentation level
_________________ ERROR collecting tests/test_fallback_data.py _________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_fallback_data.py:6: in <module>
    import modules.generate_report.fallback_data as fb
modules/generate_report/__init__.py:12: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 77
E       codex/create-comprehensive-documentation-for-fundalyze
E                                                             ^
E   IndentationError: unindent does not match any outer indentation level
________________ ERROR collecting tests/test_group_analysis.py _________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_group_analysis.py:3: in <module>
    import modules.management.group_analysis.group_analysis as ga
modules/management/__init__.py:3: in <module>
    from .portfolio_manager.portfolio_manager import main as run_portfolio_manager
E     File "/workspace/Fundalyze/modules/management/portfolio_manager/__init__.py", line 1
E       codex/create-comprehensive-documentation-for-fundalyze
E   IndentationError: unexpected indent
__________________ ERROR collecting tests/test_integration.py __________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_integration.py:7: in <module>
    import modules.management.portfolio_manager.portfolio_manager as pm
modules/management/__init__.py:3: in <module>
    from .portfolio_manager.portfolio_manager import main as run_portfolio_manager
E     File "/workspace/Fundalyze/modules/management/portfolio_manager/__init__.py", line 1
E       codex/create-comprehensive-documentation-for-fundalyze
E   IndentationError: unexpected indent
________________ ERROR collecting tests/test_interface_extra.py ________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_interface_extra.py:3: in <module>
    from modules.interface import print_table
E     File "/workspace/Fundalyze/modules/interface.py", line 1
E       codex/create-comprehensive-documentation-for-fundalyze
E                                                ^^^
E   SyntaxError: invalid syntax
______________ ERROR collecting tests/test_management_package.py _______________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_management_package.py:2: in <module>
    from modules.management import (
modules/management/__init__.py:3: in <module>
    from .portfolio_manager.portfolio_manager import main as run_portfolio_manager
E     File "/workspace/Fundalyze/modules/management/portfolio_manager/__init__.py", line 1
E       codex/create-comprehensive-documentation-for-fundalyze
E   IndentationError: unexpected indent
_______________ ERROR collecting tests/test_metadata_checker.py ________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_metadata_checker.py:6: in <module>
    import modules.generate_report.metadata_checker as mc
modules/generate_report/__init__.py:12: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 77
E       codex/create-comprehensive-documentation-for-fundalyze
E                                                             ^
E   IndentationError: unindent does not match any outer indentation level
_________________ ERROR collecting tests/test_note_manager.py __________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_note_manager.py:7: in <module>
    from management.note_manager import note_manager
modules/management/__init__.py:3: in <module>
    from .portfolio_manager.portfolio_manager import main as run_portfolio_manager
E     File "/workspace/Fundalyze/modules/management/portfolio_manager/__init__.py", line 1
E       codex/create-comprehensive-documentation-for-fundalyze
E   IndentationError: unexpected indent
________________ ERROR collecting tests/test_output_dir_env.py _________________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_output_dir_env.py:4: in <module>
    import modules.generate_report.report_generator as rg
modules/generate_report/__init__.py:12: in <module>
    from .report_generator import fetch_and_compile
E     File "/workspace/Fundalyze/modules/generate_report/report_generator.py", line 77
E       codex/create-comprehensive-documentation-for-fundalyze
E                                                             ^
E   IndentationError: unindent does not match any outer indentation level
_______________ ERROR collecting tests/test_portfolio_manager.py _______________
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/python.py:497: in importtestmodule
    mod = import_path(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/root/.pyenv/versions/3.11.12/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
tests/test_portfolio_manager.py:3: in <module>
    import modules.management.portfolio_manager.portfolio_manager as pm
modules/management/__init__.py:3: in <module>
    from .portfolio_manager.portfolio_manager import main as run_portfolio_manager
E     File "/workspace/Fundalyze/modules/management/portfolio_manager/__init__.py", line 1
E       codex/create-comprehensive-documentation-for-fundalyze
E   IndentationError: unexpected indent
=========================== short test summary info ============================
ERROR tests/test_directus_tools_init.py
ERROR tests/test_e2e.py
ERROR tests/test_excel_dashboard.py
ERROR tests/test_excel_dashboard_extra.py
ERROR tests/test_fallback_data.py
ERROR tests/test_group_analysis.py
ERROR tests/test_integration.py
ERROR tests/test_interface_extra.py
ERROR tests/test_management_package.py
ERROR tests/test_metadata_checker.py
ERROR tests/test_note_manager.py
ERROR tests/test_output_dir_env.py
ERROR tests/test_portfolio_manager.py
!!!!!!!!!!!!!!!!!!! Interrupted: 13 errors during collection !!!!!!!!!!!!!!!!!!!
13 errors in 2.59s
```
