"""
Convert a BAM file to a small SAM file
"""

import candig.common.utils as utils


@utils.Timed()
def main():
    tool = utils.AlignmentFileTool(
        utils.AlignmentFileConstants.BAM,
        utils.AlignmentFileConstants.SAM)
    tool.parseArgs()
    tool.convert()


if __name__ == '__main__':
    main()
