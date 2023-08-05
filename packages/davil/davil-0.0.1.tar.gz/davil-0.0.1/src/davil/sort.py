import re


def enumerated_file_names_sort(x, num_block_to_sort_by=0):
    """
    Key function for 'sorted'.\n
    Sorts a list of Strings according to some block of numbers in the String.\n
    E.g. file names that contain some prefix and an index: [img1_0.png, img1_1.png, img1_2.png]
    If the String contains several number blocks, the index of the number block to sort by can be
    specified with partial. E.g. sort the example list by the index in the filename
    partial(enumerated_file_names_sort, num_block_to_sort_by=1)

    :param x: input of the key function
    :param num_block_to_sort_by: the index of the number block to sort by
    :return: the num_block_to_sort_by'th number block as Int in the String x
    """
    nums = [int(s) for s in re.findall(r'\d+', x)]
    return nums[num_block_to_sort_by]


def numbered_file_names_sort(x):
    """
    Key function for 'sorted'.\n
    Sorts a list of Strings according to al numbers contained in the String.\n
    All numbers will be simply concatenated.

    :param x: input of the key function
    :return: all numbers contained in x concatenated and converted to int
    """
    nums = [s for s in re.findall(r'\d+', x)]
    num = int(''.join(nums))
    return num
