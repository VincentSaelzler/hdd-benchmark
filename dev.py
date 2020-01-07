import badblocks
import dev_info


class Dev:
    def __init__(self, dev_name, create_time):
        self.create_time = create_time
        self.dev_name = dev_name
        self.path = '/dev/' + dev_name

        self.info = dev_info.get_info(self.path)
        self.serial = dev_info.get_serial(self.path)
        self.bb_runtimes = []
        self.bad_blocks = []

    def run_badblocks(self, log_file_path):
        bb_runtime_row = badblocks.run_badblocks(self.path, log_file_path)
        self.bb_runtimes.append(bb_runtime_row)
        return bb_runtime_row

    def check_for_bad_blocks(self, log_file_path):
        bad_blocks_row = badblocks.check_for_bad_blocks(log_file_path)
        self.bad_blocks.append(bad_blocks_row)
        return bad_blocks_row
