import os
import yaml
import unittest

REQUIRED_PATHS = [
    '_config.yml',
    'index.html',
    'about.md',
    '_layouts/default.html',
    '_layouts/post.html',
    '_includes/header.html',
    '_includes/footer.html',
    '_posts',
]

class TestProjectStructure(unittest.TestCase):
    def test_paths_exist(self):
        for path in REQUIRED_PATHS:
            with self.subTest(path=path):
                self.assertTrue(os.path.exists(path), f"{path} should exist")

    def test_config_yaml(self):
        with open('_config.yml', 'r') as f:
            data = yaml.safe_load(f)
        self.assertIn('title', data)
        self.assertIn('theme', data)

    def test_post_front_matter(self):
        post_files = [f for f in os.listdir('_posts') if f.endswith('.md')]
        self.assertTrue(post_files, 'No posts found')
        for fname in post_files:
            with self.subTest(post=fname):
                with open(os.path.join('_posts', fname)) as f:
                    head = []
                    for line in f:
                        if line.strip() == '---' and head:
                            break
                        if line.strip() != '---':
                            head.append(line)
                    meta = yaml.safe_load('\n'.join(head))
                    self.assertIn('layout', meta)
                    self.assertIn('title', meta)
                    self.assertIn('date', meta)

if __name__ == '__main__':
    unittest.main()
