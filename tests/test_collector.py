import sys_mon
import sys_mon.collector as collector
from types import SimpleNamespace


def test_update_cpu_data(mocker):
    mocker.patch("sys_mon.collector.psutil.cpu_percent", return_value=[25.0, 75.0, 50.0, 100.0])

    collector.update_cpu_data()
    cpu_data = collector.get_cpu_data()

    assert cpu_data["average"] == 62.5
    assert cpu_data["cores"] == [100.0, 75.0, 50.0, 25.0]


def test_update_ram_data(mocker):
    mocker.patch("sys_mon.collector.psutil.virtual_memory", return_value=[100, 70, 30.0, 900])

    collector.update_ram_data()
    ram_data = collector.get_ram_data()

    assert ram_data["total"] == '100.0B'
    assert ram_data["available"] == '70.0B'
    assert ram_data["percent"] == 30
    assert ram_data["used"] == '900.0B'


def test_update_partitions_data(mocker):
    collector.partitions_data.clear()

    mock_partition = mocker.Mock()
    mock_partition.mountpoint = "D:\\"
    mocker.patch("sys_mon.collector.psutil.disk_partitions", return_value=[mock_partition])
    mocker.patch.object(sys_mon.collector, "get_disk_stats", return_value={"data": 0})

    collector.update_partitions_data()
    partitions_data = collector.get_partitions_data()

    assert partitions_data["D:\\"]["data"] == 0


def test_invalid_update_partitions_data(mocker):
    collector.partitions_data.clear()

    mock_partition = mocker.Mock()
    mock_partition.mountpoint = "invalid"
    mocker.patch("sys_mon.collector.psutil.disk_partitions", return_value=[mock_partition])
    mocker.patch.object(sys_mon.collector, "get_disk_stats", return_value=None)

    collector.update_partitions_data()
    partitions_data = collector.get_partitions_data()

    assert partitions_data == {}


def test_update_network_data(mocker):
    """ This test takes a while """
    start_time, end_time = 2, 9
    start_counter = {}
    end_counter = {}
    for i in range(100, 500, 100):
        start_counter[i] = SimpleNamespace(bytes_sent=5000 - i, bytes_recv=4000 - i)  # different on purpose
        end_counter[i] = SimpleNamespace(bytes_sent=5000 + i, bytes_recv=5000 + i)
    mocker.patch('sys_mon.collector.psutil.net_io_counters', side_effect=[start_counter, end_counter])
    mocker.patch('sys_mon.collector.time.time', side_effect=[start_time, end_time])

    collector.update_network_data()
    network_data = collector.get_network_data()

    assert network_data['upload'] == '285.71 Bps'
    assert network_data['download'] == '857.14 Bps'


def test_get_all_data(mocker):
    """ The logic is only in the cores -> deletes 0.0 usages. """
    mocker.patch.object(collector, "get_cpu_data", return_value={"cores": [0.0, 25.0, 0.0, 50.0, 75.0]})

    all_data = collector.get_all_data()

    assert all_data["cpu"]["cores"] == [75.0, 50.0, 25.0]
    assert all_data["ram"] == {"total": '', "used": '', "available": '', "percent": 0}
    assert all_data["partitions"] == {}
    assert all_data['network'] == {'upload': '', 'download': ''}


def test_get_disk_stats_valid_path(mocker):
    mocker.patch("sys_mon.collector.os.path.exists", return_value=True)
    mocker.patch("sys_mon.collector.psutil.disk_usage", return_value=[100, 900, 70, 30.0])

    disk_stats = collector.get_disk_stats("path")

    assert disk_stats["total"] == '100.0B'
    assert disk_stats["used"] == '900.0B'
    assert disk_stats["available"] == '70.0B'
    assert disk_stats["percent"] == 30


def test_get_disk_stats_invalid_path(mocker):
    """ Path is invalid if it doesn't exist or if it disconnects. invalid_path must be before patch os.path! """
    mocker.patch("sys_mon.logger.log_error")

    invalid_path = collector.get_disk_stats("invalid_path")  # if path doesn't exist

    mocker.patch("sys_mon.collector.os.path.exists", return_value=True)

    disconnected_path = collector.get_disk_stats("path")  # path is invalid and os is patched -> as if disconnection

    assert invalid_path is None
    assert disconnected_path is None
