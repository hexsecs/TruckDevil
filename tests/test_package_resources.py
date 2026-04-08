from importlib.resources import files


def test_json_resources_packaged():
    json_dir = files("truckdevil").joinpath("resources", "json_files")

    expected_files = [
        "pgn_list.json",
        "spn_list.json",
        "src_addr_list.json",
        "dataBitDecoding.json",
        "UDS_services.json",
        "UDS_functions.json",
        "UDS_NRC.json",
    ]

    for name in expected_files:
        assert json_dir.joinpath(name).is_file(), f"missing packaged resource: {name}"
