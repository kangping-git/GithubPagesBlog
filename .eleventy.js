module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy({
    'src/assets/images': 'assets/images',
    'src/assets/js': 'assets/js'
  });

  return {
    dir: {
      input: "src",
      output: "public",
      includes: "_includes",
      layouts: "_layouts"
    }
  };
};
