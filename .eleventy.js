const { DateTime } = require('luxon');

module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy({
    'src/assets/images': 'assets/images',
    'src/assets/js': 'assets/js'
  });

  eleventyConfig.addFilter('filterByTag', (posts, tag) => {
    return (posts || []).filter(post => Array.isArray(post.data.tags) && post.data.tags.includes(tag));
  });

  eleventyConfig.addFilter('filterByCategory', (posts, category) => {
    return (posts || []).filter(post => Array.isArray(post.data.categories) && post.data.categories.includes(category));
  });

  eleventyConfig.addFilter('date', (dateObj, format = 'yyyy-MM-dd') => {
    if(!dateObj) {
      return '';
    }
    let dt = (dateObj instanceof Date) ? DateTime.fromJSDate(dateObj) : DateTime.fromISO(dateObj.toString());
    return dt.toFormat(format);
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
