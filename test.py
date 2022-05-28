from collections import defaultdict
from random import choices, randint
from unittest import TestCase, main

from string import ascii_lowercase

from ukkonens import SuffixTree
from alphabet import printable_ascii_letters


def create_suffix_tree(string):
    return SuffixTree(string, alphabet=printable_ascii_letters)


def substring_occurrences(suffix_tree, substring) -> set[int]:
    occurrences = set()

    for i in suffix_tree.substring_occurrences(substring):
        occurrences.add(i)

    return occurrences


def suffix_occurrence(suffix_tree, suffix) -> int | None:
    return suffix_tree.contains_suffix(suffix)


def suffix_occurrence_naive(string, suffix) -> int | None:
    i = string.find(suffix)

    if len(string) - len(suffix) != i:
        return None

    return i


def substring_occurrences_naive(string, substring) -> set[int]:
    occurrences = set()

    i = string.find(substring)
    while i != -1:
        occurrences.add(i)
        i = string.find(substring, i + 1)

    return occurrences


class UkkonensTest(TestCase):
    substring_occurrences_count = defaultdict(lambda: 0)
    suffix_matches = 0
    suffix_mismatches = 0

    def create_string(self, length, character_count=26, sentinal_termianted=False):
        if sentinal_termianted:
            length -= 1

        random_characters = choices(ascii_lowercase[:character_count], k=length)

        if sentinal_termianted:
            random_characters.append("$")

        random_string = "".join(random_characters)

        return random_string

    def create_randomised_string(
        self,
        min_length,
        max_length,
        min_character_set_size,
        max_character_set_size,
        sentinal_terminated=False,
    ):
        length = randint(min_length, max_length)
        character_count = randint(min_character_set_size, max_character_set_size)

        return self.create_string(length, character_count, sentinal_terminated)

    def substring_occurrences_test(self, suffix_tree, string, pattern):
        occurrences = substring_occurrences_naive(string, pattern)
        result = substring_occurrences(suffix_tree, pattern)

        # Keep track of how many of each count of occurrences we have seen
        # Allows us to know that we are checking patterns that occur multiple times within a string,
        # so we know we aren't just checking the case where there is only one occurrence of the pattern
        self.substring_occurrences_count[len(result)] += 1

        # Set equality is independent of their ordering
        self.assertEqual(occurrences, result)

    def suffix_occurrence_test(self, suffix_tree, string, pattern):
        occurrence = suffix_occurrence_naive(string, pattern)
        result = suffix_occurrence(suffix_tree, pattern)

        if result is None:
            self.suffix_mismatches += 1
        else:
            self.suffix_matches += 1

        self.assertEqual(occurrence, result)

    def robust_test(self, string):
        """
        We are just checking that creating a suffix tree,
        with the given string, does not result in any errors
        """
        create_suffix_tree(string)

    def iterative_robust_test(
        self,
        string_count,
        min_string_length,
        max_string_length,
        min_character_set_size=3,
        max_character_set_size=26,
    ):
        for _ in range(string_count):
            random_string = self.create_randomised_string(
                min_string_length,
                max_string_length,
                min_character_set_size,
                max_character_set_size,
            )
            self.robust_test(random_string)

    def iterative_substring_test(
        self,
        string_count,
        min_string_length,
        max_string_length,
        pattern_count,
        min_pattern_length,
        max_pattern_length,
        min_character_set_size=3,
        max_character_set_size=26,
    ):
        self.substring_occurrences_count = defaultdict(lambda: 0)

        for _ in range(string_count):
            random_string = self.create_randomised_string(
                min_string_length,
                max_string_length,
                min_character_set_size,
                max_character_set_size,
                sentinal_terminated=True,
            )

            suffix_tree = create_suffix_tree(random_string)

            for _ in range(pattern_count):
                random_pattern = self.create_randomised_string(
                    min_pattern_length,
                    max_pattern_length,
                    min_character_set_size,
                    max_character_set_size,
                    sentinal_terminated=False,
                )

                self.substring_occurrences_test(
                    suffix_tree, random_string, random_pattern
                )

        print()
        print(self.substring_occurrences_count)

    def iterative_suffixes_test(
        self,
        string_count,
        min_string_length,
        max_string_length,
        pattern_count,
        min_pattern_length,
        max_pattern_length,
        min_character_set_size=3,
        max_character_set_size=26,
    ):
        self.suffix_matches = 0
        self.suffix_mismatches = 0

        for _ in range(string_count):
            random_string = self.create_randomised_string(
                min_string_length,
                max_string_length,
                min_character_set_size,
                max_character_set_size,
                sentinal_terminated=True,
            )

            suffix_tree = create_suffix_tree(random_string)

            for _ in range(pattern_count):
                random_pattern = self.create_randomised_string(
                    min_pattern_length,
                    max_pattern_length,
                    min_character_set_size,
                    max_character_set_size,
                    sentinal_terminated=True,
                )

                self.suffix_occurrence_test(suffix_tree, random_string, random_pattern)
        print()
        print("Matches:", self.suffix_matches)
        print("Mismatches:", self.suffix_mismatches)

    def test_small_string_robustness(self):
        self.iterative_robust_test(
            string_count=10000, min_string_length=5, max_string_length=10
        )

    def test_medium_string_robustness(self):
        self.iterative_robust_test(
            string_count=5000, min_string_length=20, max_string_length=50
        )

    def test_large_string_robustness(self):
        self.iterative_robust_test(
            string_count=1000, min_string_length=100, max_string_length=500
        )

    def test_massive_string_robustness(self):
        self.iterative_robust_test(
            string_count=100, min_string_length=1000, max_string_length=10000
        )

    def test_substrings(self):
        self.iterative_substring_test(
            string_count=1000,
            min_string_length=100,
            max_string_length=1000,
            pattern_count=1000,
            min_pattern_length=3,
            max_pattern_length=20,
        )

    def test_suffixes(self):
        self.iterative_suffixes_test(
            string_count=1000,
            min_string_length=20,
            max_string_length=50,
            pattern_count=1000,
            min_pattern_length=3,
            max_pattern_length=8,
            max_character_set_size=8,
        )


if __name__ == "__main__":
    main()
