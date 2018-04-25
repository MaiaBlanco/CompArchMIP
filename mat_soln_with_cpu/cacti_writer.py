# Based on xenon DSL cacti config writer
def writeAllCactiConfigs(benchmark, cacti_config_files):
    rw_ports = max(1, benchmark["tlb_bandwidth"])
    cache_params = {"cache_size": int(benchmark["cache_size"][:-2])*1024,
                    "cache_assoc": benchmark["cache_assoc"],
                    "rw_ports": rw_ports,
                    "exr_ports": 0, #params["load_bandwidth"],
                    "exw_ports": 0, #params["store_bandwidth"],
                    "line_size": benchmark["cache_line_sz"],
                    "banks" : 1, # One bank
                    "cache_type": "cache",
                    "search_ports": 0,
                    # Note for future reference - this may have to change per
                    # benchmark.
                    "io_bus_width" : 16 * 8}
    with open(cacti_config_files["cache"], "w") as f:
       writeCactiConfigFile_(f, cache_params)

    tlb_params = {"cache_size": benchmark["tlb_entries"]*8,
                  "cache_assoc": 0, #fully associative
                  "rw_ports": 0,
                  "exw_ports":  1,  # One write port for miss returns.
                  "exr_ports": rw_ports,
                  "line_size": 8,  # 64b per TLB entry. in bytes
                  "banks" : 1,
                  "cache_type": "cache",
                  "search_ports": rw_ports,
                  "io_bus_width" : 64}
    with open(cacti_config_files["tlb"], "w") as f:
       writeCactiConfigFile_(f, tlb_params)

    queue_params = {"cache_size": benchmark["cache_queue_size"]*8,
                    "cache_assoc": 0,  # fully associative
                    "rw_ports": rw_ports,
                    "exw_ports": 0,
                    "exr_ports": 0,
                    "line_size": 8,  # 64b (ignoring a few extra for status).
                    "banks" : 1,
                    "cache_type": "cache",
                    "search_ports": rw_ports,
                    "io_bus_width": 64}
    with open(cacti_config_files["queue"], "w") as f:
       writeCactiConfigFile_(f, queue_params)

def writeCactiConfigFile_(config_file, params):
    """ Writes CACTI 6.5+ config files to the provided file handle. """
    cache_size = max(64, params["cache_size"])
    config_file.write("-size (bytes) %d\n" % cache_size)
    config_file.write("-associativity %d\n" % params["cache_assoc"])
    config_file.write("-read-write port %d\n" % params["rw_ports"])
    config_file.write("-cache type \"%s\"\n" % params["cache_type"])
    config_file.write("-block size (bytes) %d\n" % params["line_size"])
    config_file.write("-search port %d\n" % params["search_ports"])
    config_file.write("-output/input bus width %d\n" % params["io_bus_width"])
    config_file.write("-exclusive write port %d\n" % params["exw_ports"])
    config_file.write("-exclusive read port %d\n" % params["exr_ports"])
    config_file.write("-UCA bank count %d\n" % params["banks"])
    # Default parameters
    config_file.write(
        "-Power Gating - \"false\"\n"
        "-Power Gating Performance Loss 0.01\n"
        "-single ended read ports 0\n"
        "-technology (u) 0.040\n"
        "-page size (bits) 8192 \n"
        "-burst length 8\n"
        "-internal prefetch width 8\n"
        "-Data array cell type - \"itrs-hp\"\n"
        "-Tag array cell type - \"itrs-hp\"\n"
        "-Data array peripheral type - \"itrs-hp\"\n"
        "-Tag array peripheral type - \"itrs-hp\"\n"
        "-hp Vdd (V) \"default\"\n"
        "-lstp Vdd (V) \"default\"\n"
        "-lop Vdd (V) \"default\"\n"
        "-Long channel devices - \"true\"\n"
        "-operating temperature (K) 300\n"
        "-tag size (b) \"default\"\n"
        "-access mode (normal, sequential, fast) - \"normal\"\n"
        "-design objective (weight delay, dynamic power, leakage power, "
            "cycle time, area) 0:0:100:0:0\n"
        "-deviate (delay, dynamic power, leakage power, cycle time, area) "
            "20:100000:100000:100000:100000\n"
        "-NUCAdesign objective (weight delay, dynamic power, leakage power, "
            "cycle time, area) 100:100:0:0:100\n"
        "-NUCAdeviate (delay, dynamic power, leakage power, cycle time, area) "
            "10:10000:10000:10000:10000\n"
        "-Optimize ED or ED^2 (ED, ED^2, NONE): \"NONE\"\n"
        "-Cache model (NUCA, UCA)  - \"UCA\"\n"
        "-NUCA bank count 0\n"
        "-Wire signalling (fullswing, lowswing, default) - \"Global_30\"\n"
        "-Wire inside mat - \"semi-global\"\n"
        "-Wire outside mat - \"semi-global\"\n"
        "-Interconnect projection - \"conservative\"\n"
        "-Core count 1\n"
        "-Cache level (L2/L3) - \"L2\"\n"
        "-Add ECC - \"false\"\n"
        "-Print level (DETAILED, CONCISE) - \"DETAILED\"\n"
        "-Print input parameters - \"false\"\n"
        "-Force cache config - \"false\"\n"
        "-Ndwl 1\n"
        "-Ndbl 1\n"
        "-Nspd 0\n"
        "-Ndcm 1\n"
        "-Ndsam1 0\n"
        "-Ndsam2 0\n")
