import unittest

from pyjarowinkler.comparative import Comparative

__author__ = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"


class TestComparative(unittest.TestCase):
    def setUp(self) -> None:
        self.comparative = Comparative("dummy_string_1", "dummy_string_2")

    def test_sanitize_exception(self) -> None:
        with self.assertRaises(ValueError):
            Comparative(None, None)  # type: ignore

    def test_sanitize_exception_args(self) -> None:
        with self.assertRaises(ValueError):
            Comparative("4", 333)  # type: ignore

    def test_sanitize_spaces(self) -> None:
        comparative: Comparative = Comparative("   asdf ", "asdf     ")
        self.assertEqual([comparative.first, comparative.second], ["asdf", "asdf"])

    def test_ascii_letters_unchanged(self):
        for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            with self.subTest(char=char):
                self.assertEqual(self.comparative._sanitize(char, norm_ambiguous=True), char)

    def test_ascii_numbers_unchanged(self):
        for char in "0123456789":
            with self.subTest(char=char):
                self.assertEqual(self.comparative._sanitize(char, norm_ambiguous=True), char)

    def test_ascii_symbols_unchanged(self):
        symbols = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        for char in symbols:
            with self.subTest(char=char):
                self.assertEqual(self.comparative._sanitize(char, norm_ambiguous=True), char)

    def test_ascii_whitespace_unchanged(self):
        self.assertEqual(self.comparative._sanitize(" ", norm_ambiguous=True), "")
        self.assertEqual(self.comparative._sanitize("\t", norm_ambiguous=True), "")
        self.assertEqual(self.comparative._sanitize("\n", norm_ambiguous=True), "")

    def test_cyrillic_to_latin(self):
        test_cases = [
            ("А", "A"),  # Cyrillic A
            ("а", "a"),  # Cyrillic a
            ("Е", "E"),  # Cyrillic E
            ("е", "e"),  # Cyrillic e
            ("О", "O"),  # Cyrillic O
            ("о", "o"),  # Cyrillic o
        ]
        for cyrillic, latin in test_cases:
            with self.subTest(cyrillic=cyrillic, latin=latin):
                self.assertEqual(self.comparative._sanitize(cyrillic, norm_ambiguous=True), latin)

    def test_greek_to_latin(self):
        test_cases = [
            ("Α", "A"),  # Greek Alpha
            ("α", "a"),  # Greek alpha
            ("Ε", "E"),  # Greek Epsilon
            ("ο", "o"),  # Greek omicron
        ]
        for greek, latin in test_cases:
            with self.subTest(greek=greek, latin=latin):
                self.assertEqual(self.comparative._sanitize(greek, norm_ambiguous=True), latin)

    def test_accented_to_base(self):
        test_cases = [
            ("à", "a"),
            ("á", "a"),
            ("â", "a"),
            ("è", "e"),
            ("é", "e"),
            ("ê", "e"),
            ("À", "A"),
            ("Á", "A"),
            ("Â", "A"),
        ]
        for accented, base in test_cases:
            with self.subTest(accented=accented, base=base):
                self.assertEqual(self.comparative._sanitize(accented, norm_ambiguous=True), base)

    def test_unmapped_unicode_unchanged(self):
        unmapped_chars = ["€", "£", "¥", "©", "®", "™", "→", "✓", "★"]
        for char in unmapped_chars:
            with self.subTest(char=char):
                self.assertEqual(self.comparative._sanitize(char, norm_ambiguous=True), char)

    def test_pure_ascii_string_unchanged(self):
        test_strings = [
            "hello",
            "world",
            "test123",
            "Hello World!",
            "email@example.com",
        ]
        for text in test_strings:
            with self.subTest(text=text):
                self.assertEqual(self.comparative._sanitize(text, norm_ambiguous=True), text)

    def test_cyrillic_word_normalization(self):
        test_cases = [
            ("pаypal", "paypal"),  # Cyrillic 'а'
            ("Аpple", "Apple"),  # Cyrillic 'А'
            ("gооgle", "google"),  # Cyrillic 'о's
            ("Microsоft", "Microsoft"),  # Cyrillic 'о'
        ]
        for cyrillic_word, expected in test_cases:
            with self.subTest(input=cyrillic_word, expected=expected):
                self.assertEqual(self.comparative._sanitize(cyrillic_word, norm_ambiguous=True), expected)

    def test_greek_word_normalization(self):
        test_cases = [
            ("αpple", "apple"),  # Greek alpha
            ("gοοgle", "google"),  # Greek omicrons
            ("Αmazon", "Amazon"),  # Greek Alpha
        ]
        for greek_word, expected in test_cases:
            with self.subTest(input=greek_word, expected=expected):
                self.assertEqual(self.comparative._sanitize(greek_word, norm_ambiguous=True), expected)

    def test_accented_word_normalization(self):
        test_cases = [
            ("café", "cafe"),
            ("naïve", "naive"),
            ("résumé", "resume"),
            ("À propos", "A propos"),
        ]
        for accented, expected in test_cases:
            with self.subTest(input=accented, expected=expected):
                self.assertEqual(self.comparative._sanitize(accented, norm_ambiguous=True), expected)

    def test_mixed_homoglyphs_normalization(self):
        test_cases = [
            ("pаypαl", "paypal"),  # Cyrillic 'а' + Greek 'α'
            ("gооglе", "google"),  # Cyrillic 'о's and 'е'
            ("Аmαzοn", "Amazon"),  # Mixed Cyrillic and Greek
        ]
        for mixed, expected in test_cases:
            with self.subTest(input=mixed, expected=expected):
                self.assertEqual(self.comparative._sanitize(mixed, norm_ambiguous=True), expected)

    def test_partial_homoglyph_normalization(self):
        test_cases = [
            ("pаypal.com", "paypal.com"),  # Only 'а' changes
            ("user@еxample.com", "user@example.com"),  # Only 'е' changes
            ("hello_wοrld", "hello_world"),  # Only 'ο' changes
        ]
        for input_str, expected in test_cases:
            with self.subTest(input=input_str, expected=expected):
                self.assertEqual(self.comparative._sanitize(input_str, norm_ambiguous=True), expected)

    def test_unicode_preservation(self):
        test_cases = [
            ("test™", "test™"),
            ("price: €100", "price: €100"),
            ("hello→world", "hello→world"),
        ]
        for text, expected in test_cases:
            with self.subTest(text=text):
                self.assertEqual(self.comparative._sanitize(text, norm_ambiguous=True), expected)

    def test_single_character_strings(self):
        test_cases = [
            ("a", "a"),
            ("А", "A"),  # Cyrillic
            ("α", "a"),  # Greek
            ("à", "a"),  # Accented
        ]
        for char, expected in test_cases:
            with self.subTest(char=char):
                self.assertEqual(self.comparative._sanitize(char, norm_ambiguous=True), expected)

    def test_repeated_homoglyphs(self):
        test_cases = [
            ("ааа", "aaa"),  # Triple Cyrillic 'а'
            ("ООО", "OOO"),  # Triple Cyrillic 'О'
            ("ααα", "aaa"),  # Triple Greek 'α'
        ]
        for repeated, expected in test_cases:
            with self.subTest(input=repeated, expected=expected):
                self.assertEqual(self.comparative._sanitize(repeated, norm_ambiguous=True), expected)

    def test_whitespace_with_homoglyphs(self):
        test_cases = [
            ("pаypal account", "paypal account"),
            ("hello   wοrld", "hello   world"),
            ("\tАpple\n", "Apple"),
        ]
        for text, expected in test_cases:
            with self.subTest(text=text):
                self.assertEqual(self.comparative._sanitize(text, norm_ambiguous=True), expected)

    def test_all_homoglyphs_word(self):
        all_homoglyphs = "РАΓРΑL"  # Cyrillic Р, А, Greek Γ, Р, Greek Α, Latin L
        result = self.comparative._sanitize(all_homoglyphs, norm_ambiguous=True)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), len(all_homoglyphs))

    def test_case_sensitivity(self):
        test_cases = [
            ("Pаypal", "Paypal"),  # Cyrillic 'а' → 'a' (lowercase)
            ("PАYPAL", "PAYPAL"),  # Cyrillic 'А' → 'A' (uppercase)
            ("pАypal", "pAypal"),  # Mixed case preserved
        ]
        for input_str, expected in test_cases:
            with self.subTest(input=input_str, expected=expected):
                self.assertEqual(self.comparative._sanitize(input_str, norm_ambiguous=True), expected)

    def test_common_phishing_domains(self):
        phishing_examples = [
            ("pаypal", "paypal"),  # Cyrillic 'а'
            ("αpple", "apple"),  # Greek alpha
            ("gооgle", "google"),  # Cyrillic 'о's
            ("аmazon", "amazon"),  # Cyrillic 'а'
            ("fаcebook", "facebook"),  # Cyrillic 'а'
            ("microsоft", "microsoft"),  # Cyrillic 'о'
        ]
        for phishing, legitimate in phishing_examples:
            with self.subTest(phishing=phishing, legitimate=legitimate):
                normalized = self.comparative._sanitize(phishing, norm_ambiguous=True)
                self.assertEqual(normalized, legitimate, f"Phishing attempt '{phishing}' should normalize to '{legitimate}'")
