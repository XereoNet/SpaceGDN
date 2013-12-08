module.exports = function(grunt) {

  grunt.initConfig({
    coffee: {
      dist: {
        expand: true,
        cwd: 'src',
        src: ['**/*.coffee'],
        dest: '.tmp/js',
        ext: '.js'
      }
    },
    uglify: {
      options: {
        banner: '/*! Built with Grunt */',
        compress: false
      },
      dist: {
        files: [{
          expand: true,
          cwd: '.tmp/js',
          src: ['**/*.js'],
          dest: 'dist',
          ext: '.js'
        }, {
          expand: true,
          cwd: 'src',
          src: ['**/*.js'],
          dest: 'dist',
          ext: '.js'
        }]
      }
    },
    less: {
      dist: {
        options: {
          yuicompress: true,
          concat: false
        },
        files: [{
          expand: true,
          cwd: 'src',
          src: ['**/*.less'],
          dest: 'dist',
          ext: '.css'
        }]
      }
    },
    copy: {
      app: {
        files: [{
          expand: true,
          cwd: 'app',
          src: ['**/*.*'],
          dest: 'dist'
        }]
      },
    },
    imagemin: {
      dist: {
        options: {
          removeComments: true
        },
        files: [{
          expand: true,
          cwd: 'src',
          src: ['**/*.{png,jpg,jpeg}'],
          dest: 'dist',
        }]
      }
    },
    concurrent: {
      build: ['coffee', 'less', 'copy', 'imagemin']
    },
    clean: {
      pre: ['dist'],
      post: ['.tmp']
    }
  });

  grunt.loadNpmTasks('grunt-concurrent');
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-imagemin');

  grunt.registerTask('default', ['clean:pre', 'concurrent:build', 'uglify', 'clean:post']);

};