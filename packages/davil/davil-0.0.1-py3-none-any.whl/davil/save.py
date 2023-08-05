from abc import ABC, abstractmethod
from typing import List
import numpy as np

from src.davil.paths import check_slash, check_extension_dot
from src.davil.types import is_list


class Saver(ABC):
    def __init__(self, dir_path, start_counter=0):
        self.dir_path = dir_path
        self.counter = start_counter

    def save_next(self, obj):
        self._save_func(obj)
        self.counter = self.counter + 1

    @abstractmethod
    def _save_func(self, obj):
        raise NotImplementedError()


class PilImageSaver(Saver):
    def __init__(self, dir_path, name, file_extension, start_counter=0):
        super().__init__(dir_path, start_counter)
        self.name = name
        self.file_extension = file_extension

    def _save_func(self, pil_image):
        pil_image.save(
            check_slash(self.dir_path) + self.name + str(self.counter) + check_extension_dot(self.file_extension))


class ArraySaver(Saver):
    def __init__(self, dir_path, name, start_counter=0, d_type=None, compressed=False):
        super().__init__(dir_path, start_counter)
        self.compressed = compressed
        self.name = name
        if d_type is None:
            self.conversion = lambda x: x
        else:
            self.conversion = d_type

    def _save_func(self, arr):
        if self.compressed:
            np.savez_compressed(
                check_slash(self.dir_path) + self.name + str(self.counter),
                self.conversion(arr))
        else:
            np.save(check_slash(self.dir_path) + self.name + str(self.counter) + check_extension_dot('.npy'),
                    self.conversion(arr))


class Savers(object):
    def __init__(self):
        self.savers: List[Saver] = []

    def save_next(self, obj):
        for saver, o in zip(self.savers, obj):
            saver.save_next(o)


class PilImageSavers(Savers):
    def __init__(self, dir_path, names, file_extensions, start_counter=0):
        super().__init__()

        exts = file_extensions
        if not is_list(file_extensions):
            if isinstance(exts, str):
                exts = [exts] * len(names)

        for name, ext in zip(names, exts):
            self.savers.append(PilImageSaver(dir_path, name, ext, start_counter))


class ArraySavers(Savers):
    def __init__(self, dir_path, names, d_types, compressed=False, start_counter=0):
        super().__init__()

        conversions = d_types
        if not is_list(conversions):
            # TODO: hackedy hack, what is the correct way to determine if something is a numpy dtype?
            if isinstance(type(conversions), type(np.uint8)):
                conversions = [conversions] * len(names)

        for name, conv in zip(names, conversions):
            self.savers.append(ArraySaver(dir_path, name, start_counter, d_type=conv, compressed=compressed))
