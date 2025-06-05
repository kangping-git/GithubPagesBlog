import os
import yaml
import json
import unittest

REQUIRED_PATHS = [
    'package.json',
    '.eleventy.js',
    'src/index.md',
    'src/about.md',
    'src/_layouts/base.njk',
    'src/_layouts/post.njk',
    'src/_includes/header.njk',
    'src/_includes/footer.njk',
    'src/posts',
]

class TestProjectStructure(unittest.TestCase):
    def test_paths_exist(self):
        for path in REQUIRED_PATHS:
            with self.subTest(path=path):
                self.assertTrue(os.path.exists(path), f"{path} should exist")

    def test_package_json(self):
        with open('package.json') as f:
            data = json.load(f)
        deps = {}
        deps.update(data.get('dependencies', {}))
        deps.update(data.get('devDependencies', {}))
        self.assertIn('@11ty/eleventy', deps)

    def test_post_front_matter(self):
        post_files = [f for f in os.listdir('src/posts') if f.endswith('.md')]
        self.assertTrue(post_files, 'No posts found')
        for fname in post_files:
            with self.subTest(post=fname):
                with open(os.path.join('src/posts', fname)) as f:
                    head = []
                    for line in f:
                        if line.strip() == '---' and head:
                            break
                        if line.strip() != '---':
                            head.append(line.rstrip())
                    meta = yaml.safe_load('\n'.join(head))
                    self.assertIn('layout', meta)
                    self.assertIn('title', meta)
                    self.assertIn('date', meta)

if __name__ == '__main__':
    unittest.main()
