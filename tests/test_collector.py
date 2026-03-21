import sys
import src.collector as collector

sys.path.insert(0, "../src")  # so it will recognise src.collector


def test_update_cpu_data(mocker):
    mocker.patch("collector.psutil.cpu_percent", return_value=[25.0, 75.0, 50.0, 100.0])

    collector.update_cpu_percentage()
    result = collector.get_cpu_data()

    assert result["average"] == 62.5
    assert result["cores"] == [100.0, 75.0, 50.0, 25.0]


def test_update_ram_data(mocker):
    mocker.patch("collector.psutil.virtual_memory", return_value=[100, 70, 30.0, 900])

    collector.update_ram_stats()
    result = collector.get_ram_data()

    assert result["total"] == '100.0B'
    assert result["available"] == '70.0B'
    assert result["percent"] == 30
    assert result["used"] == '900.0B'


def test_update_partitions_data(mocker):
    collector.partitions_data.clear()

    mock_partition = mocker.Mock()
    mock_partition.mountpoint = "D:\\"
    mocker.patch("collector.psutil.disk_partitions", return_value=[mock_partition])
    mocker.patch.object(collector, "get_disk_stats", return_value={  # because it is an internal function
        "total": "700.0B",
        "used": "1000.0B",
        "available": "800.0B",
        "percent": 90.0
    })

    collector.update_partitions_stats()
    result = collector.get_partitions_data()

    disk_stats = result["D:\\"]
    assert disk_stats["total"] == '700.0B'
    assert disk_stats["used"] == '1000.0B'
    assert disk_stats["available"] == '800.0B'
    assert disk_stats["percent"] == 90.0


def test_get_all_data(mocker):
    mocker.patch.object(collector, "get_cpu_data", return_value={"cores": [0.0, 25.0, 0.0, 50.0, 75.0, 100.0]})
    mocker.patch.object(collector, "get_ram_data", return_value={})
    mocker.patch.object(collector, "get_partitions_data", return_value={})

    result = collector.get_all_data()

    assert result["cpu"]["cores"] == [100.0, 75.0, 50.0, 25.0]


def test_get_disk_stats(mocker):
    mocker.patch("collector.os.path.exists", return_value=True)
    mocker.patch("collector.psutil.disk_usage", return_value=[100, 900, 70, 30.0])

    result = collector.get_disk_stats("path")

    assert result["total"] == '100.0B'
    assert result["used"] == '900.0B'
    assert result["available"] == '70.0B'
    assert result["percent"] == 30
