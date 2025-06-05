# Agent Instructions

This repository contains the Fundalyze Python application. The directory layout:

- `modules/` – core packages with data fetching utilities and portfolio management.
- `scripts/` – entry points including `main.py` for the CLI.
- `tests/` – pytest suite that covers core functionality.

## Expected Behavior

When modifying or adding any Python code or documentation, run the test suite:

```bash
pytest -q
```

All tests should pass before committing changes.

Provide concise commit messages and include PR summaries referencing relevant lines when describing changes.



## Recent Findings

```
........................................................................ [ 71%]
.............................                                            [100%]
101 passed in 4.93s
```


## Recent Findings

```
........................................................................ [ 67%]
..................................                                       [100%]
106 passed in 2.56s
```

## Recent Findings

```

........................................................................ [ 63%]
..........................................                               [100%]
=============================== warnings summary ===============================
tests/test_portfolio_manager.py::test_add_new_ticker_with_nas_present
tests/test_portfolio_manager.py::test_add_ticker_to_all_na_column
  /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py:266: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
    portfolio = pd.concat([portfolio, new_row], ignore_index=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html


## Recent Findings

```
........................................................................ [ 63%]
..........................................                               [100%]
=============================== warnings summary ===============================
tests/test_portfolio_manager.py::test_add_new_ticker_with_nas_present
tests/test_portfolio_manager.py::test_add_ticker_to_all_na_column
  /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py:266: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
    portfolio = pd.concat([portfolio, new_row], ignore_index=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html


## 🧪 Pytest Results
```
............................................FF.......................... [ 61%]
...............................F..............                           [100%]
=================================== FAILURES ===================================
______________________ test_report_generation_end_to_end _______________________

tmp_path = PosixPath('/tmp/pytest-of-root/pytest-0/test_report_generation_end_to_0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x7ff796f04410>

    def test_report_generation_end_to_end(tmp_path, monkeypatch):
        profile_df = pd.DataFrame({
            "symbol": ["AAA"],
            "sector": ["Tech"],
            "industry": ["Software"],
        })
        price_df = pd.DataFrame({
            "Date": pd.date_range("2023-01-01", periods=2),
            "Open": [1, 2],
            "High": [1, 2],
            "Low": [1, 2],
            "Close": [1, 2],
            "Adj Close": [1, 2],
            "Volume": [10, 20],
        })
        stmt_df = pd.DataFrame(
            {"Revenue": [100], "EPS": [5]}, index=pd.Index(["2023"], name="Period")
        )
    
        class FakeEquity:
            def __init__(self):
                class _Profile:
                    def __call__(self, symbol):
                        return Dummy(profile_df)
    
                class _Price:
                    def historical(self, symbol, period, provider=None):
                        return Dummy(price_df)
    
                class _Fundamental:
                    def income(self, symbol, period):
                        return Dummy(stmt_df)
    
                    def balance(self, symbol, period):
                        return Dummy(stmt_df)
    
                    def cash(self, symbol, period):
                        return Dummy(stmt_df)
    
                self.profile = _Profile()
                self.price = _Price()
                self.fundamental = _Fundamental()
    
        class FakeOBB:
            def __init__(self):
                self.equity = FakeEquity()
    
        monkeypatch.setattr(rg, "obb", FakeOBB())
    
        rg.fetch_and_compile("AAA", base_output=str(tmp_path))
        ticker_dir = tmp_path / "AAA"
>       assert (ticker_dir / "profile.csv").is_file()
E       AssertionError: assert False
E        +  where False = is_file()
E        +    where is_file = (PosixPath('/tmp/pytest-of-root/pytest-0/test_report_generation_end_to_0/AAA') / 'profile.csv').is_file

tests/test_e2e.py:68: AssertionError
----------------------------- Captured stdout call -----------------------------
Warning uploading to Directus: Object of type Timestamp is not JSON serializable
✅ Completed report for AAA (uploaded to Directus)
------------------------------ Captured log call -------------------------------
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/companies | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/companies | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/price_history | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/income_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/income_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/income_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/income_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/balance_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/balance_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/balance_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/balance_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/cash_flow | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/cash_flow | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/cash_flow | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/cash_flow | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
____________________ test_portfolio_manager_cli_end_to_end _____________________

tmp_path = PosixPath('/tmp/pytest-of-root/pytest-0/test_portfolio_manager_cli_end0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x7ff796fefa90>

    def test_portfolio_manager_cli_end_to_end(tmp_path, monkeypatch):
        data = {
            "Ticker": "AAA",
            "Name": "Alpha",
            "Sector": "Tech",
            "Industry": "Software",
            "Current Price": 10.0,
            "Market Cap": 100,
            "PE Ratio": 20.0,
            "Dividend Yield": 0.01,
        }
        monkeypatch.setattr(pm, "PORTFOLIO_FILE", str(tmp_path / "portfolio.xlsx"))
        monkeypatch.setattr(pm, "fetch_from_yfinance", lambda t: data)
    
        inputs = iter([
            "2",       # choose Add ticker
            "AAA",     # ticker list
            "y",       # accept info
            "5",       # exit
        ])
        monkeypatch.setattr("builtins.input", lambda *_args: next(inputs))
    
        pm.main()
    
>       df = pd.read_excel(pm.PORTFOLIO_FILE)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test_e2e.py:107: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/pandas/io/excel/_base.py:495: in read_excel
    io = ExcelFile(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/pandas/io/excel/_base.py:1550: in __init__
    ext = inspect_excel_format(
/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/pandas/io/excel/_base.py:1402: in inspect_excel_format
    with get_handle(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

path_or_buf = '/tmp/pytest-of-root/pytest-0/test_portfolio_manager_cli_end0/portfolio.xlsx'
mode = 'rb'

    @doc(compression_options=_shared_docs["compression_options"] % "path_or_buf")
    def get_handle(
        path_or_buf: FilePath | BaseBuffer,
        mode: str,
        *,
        encoding: str | None = None,
        compression: CompressionOptions | None = None,
        memory_map: bool = False,
        is_text: bool = True,
        errors: str | None = None,
        storage_options: StorageOptions | None = None,
    ) -> IOHandles[str] | IOHandles[bytes]:
        """
        Get file handle for given path/buffer and mode.
    
        Parameters
        ----------
        path_or_buf : str or file handle
            File path or object.
        mode : str
            Mode to open path_or_buf with.
        encoding : str or None
            Encoding to use.
        {compression_options}
    
               May be a dict with key 'method' as compression mode
               and other keys as compression options if compression
               mode is 'zip'.
    
               Passing compression options as keys in dict is
               supported for compression modes 'gzip', 'bz2', 'zstd' and 'zip'.
    
            .. versionchanged:: 1.4.0 Zstandard support.
    
        memory_map : bool, default False
            See parsers._parser_params for more information. Only used by read_csv.
        is_text : bool, default True
            Whether the type of the content passed to the file/buffer is string or
            bytes. This is not the same as `"b" not in mode`. If a string content is
            passed to a binary file/buffer, a wrapper is inserted.
        errors : str, default 'strict'
            Specifies how encoding and decoding errors are to be handled.
            See the errors argument for :func:`open` for a full list
            of options.
        storage_options: StorageOptions = None
            Passed to _get_filepath_or_buffer
    
        Returns the dataclass IOHandles
        """
        # Windows does not default to utf-8. Set to utf-8 for a consistent behavior
        encoding = encoding or "utf-8"
    
        errors = errors or "strict"
    
        # read_csv does not know whether the buffer is opened in binary/text mode
        if _is_binary_mode(path_or_buf, mode) and "b" not in mode:
            mode += "b"
    
        # validate encoding and errors
        codecs.lookup(encoding)
        if isinstance(errors, str):
            codecs.lookup_error(errors)
    
        # open URLs
        ioargs = _get_filepath_or_buffer(
            path_or_buf,
            encoding=encoding,
            compression=compression,
            mode=mode,
            storage_options=storage_options,
        )
    
        handle = ioargs.filepath_or_buffer
        handles: list[BaseBuffer]
    
        # memory mapping needs to be the first step
        # only used for read_csv
        handle, memory_map, handles = _maybe_memory_map(handle, memory_map)
    
        is_path = isinstance(handle, str)
        compression_args = dict(ioargs.compression)
        compression = compression_args.pop("method")
    
        # Only for write methods
        if "r" not in mode and is_path:
            check_parent_directory(str(handle))
    
        if compression:
            if compression != "zstd":
                # compression libraries do not like an explicit text-mode
                ioargs.mode = ioargs.mode.replace("t", "")
            elif compression == "zstd" and "b" not in ioargs.mode:
                # python-zstandard defaults to text mode, but we always expect
                # compression libraries to use binary mode.
                ioargs.mode += "b"
    
            # GZ Compression
            if compression == "gzip":
                if isinstance(handle, str):
                    # error: Incompatible types in assignment (expression has type
                    # "GzipFile", variable has type "Union[str, BaseBuffer]")
                    handle = gzip.GzipFile(  # type: ignore[assignment]
                        filename=handle,
                        mode=ioargs.mode,
                        **compression_args,
                    )
                else:
                    handle = gzip.GzipFile(
                        # No overload variant of "GzipFile" matches argument types
                        # "Union[str, BaseBuffer]", "str", "Dict[str, Any]"
                        fileobj=handle,  # type: ignore[call-overload]
                        mode=ioargs.mode,
                        **compression_args,
                    )
    
            # BZ Compression
            elif compression == "bz2":
                # Overload of "BZ2File" to handle pickle protocol 5
                # "Union[str, BaseBuffer]", "str", "Dict[str, Any]"
                handle = get_bz2_file()(  # type: ignore[call-overload]
                    handle,
                    mode=ioargs.mode,
                    **compression_args,
                )
    
            # ZIP Compression
            elif compression == "zip":
                # error: Argument 1 to "_BytesZipFile" has incompatible type
                # "Union[str, BaseBuffer]"; expected "Union[Union[str, PathLike[str]],
                # ReadBuffer[bytes], WriteBuffer[bytes]]"
                handle = _BytesZipFile(
                    handle, ioargs.mode, **compression_args  # type: ignore[arg-type]
                )
                if handle.buffer.mode == "r":
                    handles.append(handle)
                    zip_names = handle.buffer.namelist()
                    if len(zip_names) == 1:
                        handle = handle.buffer.open(zip_names.pop())
                    elif not zip_names:
                        raise ValueError(f"Zero files found in ZIP file {path_or_buf}")
                    else:
                        raise ValueError(
                            "Multiple files found in ZIP file. "
                            f"Only one file per ZIP: {zip_names}"
                        )
    
            # TAR Encoding
            elif compression == "tar":
                compression_args.setdefault("mode", ioargs.mode)
                if isinstance(handle, str):
                    handle = _BytesTarFile(name=handle, **compression_args)
                else:
                    # error: Argument "fileobj" to "_BytesTarFile" has incompatible
                    # type "BaseBuffer"; expected "Union[ReadBuffer[bytes],
                    # WriteBuffer[bytes], None]"
                    handle = _BytesTarFile(
                        fileobj=handle, **compression_args  # type: ignore[arg-type]
                    )
                assert isinstance(handle, _BytesTarFile)
                if "r" in handle.buffer.mode:
                    handles.append(handle)
                    files = handle.buffer.getnames()
                    if len(files) == 1:
                        file = handle.buffer.extractfile(files[0])
                        assert file is not None
                        handle = file
                    elif not files:
                        raise ValueError(f"Zero files found in TAR archive {path_or_buf}")
                    else:
                        raise ValueError(
                            "Multiple files found in TAR archive. "
                            f"Only one file per TAR archive: {files}"
                        )
    
            # XZ Compression
            elif compression == "xz":
                # error: Argument 1 to "LZMAFile" has incompatible type "Union[str,
                # BaseBuffer]"; expected "Optional[Union[Union[str, bytes, PathLike[str],
                # PathLike[bytes]], IO[bytes]], None]"
                handle = get_lzma_file()(
                    handle, ioargs.mode, **compression_args  # type: ignore[arg-type]
                )
    
            # Zstd Compression
            elif compression == "zstd":
                zstd = import_optional_dependency("zstandard")
                if "r" in ioargs.mode:
                    open_args = {"dctx": zstd.ZstdDecompressor(**compression_args)}
                else:
                    open_args = {"cctx": zstd.ZstdCompressor(**compression_args)}
                handle = zstd.open(
                    handle,
                    mode=ioargs.mode,
                    **open_args,
                )
    
            # Unrecognized Compression
            else:
                msg = f"Unrecognized compression type: {compression}"
                raise ValueError(msg)
    
            assert not isinstance(handle, str)
            handles.append(handle)
    
        elif isinstance(handle, str):
            # Check whether the filename is to be opened in binary mode.
            # Binary mode does not support 'encoding' and 'newline'.
            if ioargs.encoding and "b" not in ioargs.mode:
                # Encoding
                handle = open(
                    handle,
                    ioargs.mode,
                    encoding=ioargs.encoding,
                    errors=errors,
                    newline="",
                )
            else:
                # Binary mode
>               handle = open(handle, ioargs.mode)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^
E               FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-root/pytest-0/test_portfolio_manager_cli_end0/portfolio.xlsx'

/root/.pyenv/versions/3.11.12/lib/python3.11/site-packages/pandas/io/common.py:882: FileNotFoundError
----------------------------- Captured stdout call -----------------------------

=== 📈 Portfolio Manager ===
Choose an action:
  1) View portfolio
  2) Add ticker(s)
  3) Update ticker data
  4) Remove ticker
  5) Exit
  → Fetched data for AAA:
      Name         : Alpha
      Sector       : Tech
      Industry     : Software
      Current Price: 10.0
      Market Cap   : 100
      PE Ratio     : 20.0
      Dividend Yld : 0.01
  ✓ Added 'AAA' to portfolio.

→ Saved portfolio to Directus collection 'portfolio'.

Choose an action:
  1) View portfolio
  2) Add ticker(s)
  3) Update ticker data
  4) Remove ticker
  5) Exit
Exiting Portfolio Manager.
------------------------------ Captured log call -------------------------------
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/portfolio | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/portfolio | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/portfolio | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
_____________________________ test_env_output_dir ______________________________

tmp_path = PosixPath('/tmp/pytest-of-root/pytest-0/test_env_output_dir0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x7ff7969fe710>

    def test_env_output_dir(tmp_path, monkeypatch):
        profile_df = pd.DataFrame({"symbol": ["AAA"]})
        price_df = pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=1)})
        stmt_df = pd.DataFrame({"Revenue": [1]}, index=pd.Index(["2023"], name="Period"))
    
        class FakeEquity:
            def __init__(self):
                class _Profile:
                    def __call__(self, symbol):
                        return Dummy(profile_df)
    
                class _Price:
                    def historical(self, symbol, period, provider=None):
                        return Dummy(price_df)
    
                class _Fundamental:
                    def income(self, symbol, period):
                        return Dummy(stmt_df)
    
                    def balance(self, symbol, period):
                        return Dummy(stmt_df)
    
                    def cash(self, symbol, period):
                        return Dummy(stmt_df)
    
                self.profile = _Profile()
                self.price = _Price()
                self.fundamental = _Fundamental()
    
        class FakeOBB:
            def __init__(self):
                self.equity = FakeEquity()
    
        monkeypatch.setattr(rg, "obb", FakeOBB())
        monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
        rg.fetch_and_compile("AAA")
>       assert (tmp_path / "AAA" / "profile.csv").is_file()
E       AssertionError: assert False
E        +  where False = is_file()
E        +    where is_file = ((PosixPath('/tmp/pytest-of-root/pytest-0/test_env_output_dir0') / 'AAA') / 'profile.csv').is_file

tests/test_output_dir_env.py:50: AssertionError
----------------------------- Captured stdout call -----------------------------
Warning uploading to Directus: Object of type Timestamp is not JSON serializable
✅ Completed report for AAA (uploaded to Directus)
------------------------------ Captured log call -------------------------------
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/companies | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/companies | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/price_history | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/income_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/income_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/income_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/income_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/balance_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/balance_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/balance_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/balance_statement | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/cash_flow | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/cash_flow | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/fields/cash_flow | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
ERROR    modules.data.directus_client:directus_client.py:76 Invalid JSON response: Expecting value: line 1 column 1 (char 0) | URL: https://api.veralims.com/items/cash_flow | Content: <!DOCTYPE html>
<html>
  <head>
    <title>Sign in ã» Cloudflare Access</title>
    <meta charset="
=============================== warnings summary ===============================
tests/test_portfolio_manager.py::test_add_new_ticker_with_nas_present
tests/test_portfolio_manager.py::test_add_ticker_to_all_na_column
  /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py:265: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
    portfolio = pd.concat([portfolio, new_row], ignore_index=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_e2e.py::test_report_generation_end_to_end - AssertionError:...
FAILED tests/test_e2e.py::test_portfolio_manager_cli_end_to_end - FileNotFoun...
FAILED tests/test_output_dir_env.py::test_env_output_dir - AssertionError: as...
3 failed, 115 passed, 2 warnings in 20.99s
```
