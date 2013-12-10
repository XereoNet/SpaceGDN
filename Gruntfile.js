module.exports = function(grunt) {

  grunt.initConfig({
    coffee: {
      app: {
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
      app: {
        files: [{
          expand: true,
          cwd: '.tmp/js',
          src: ['**/*.js'],
          dest: 'app',
          ext: '.js'
        }, {
          expand: true,
          cwd: 'src',
          src: ['**/*.js'],
          dest: 'app',
          ext: '.js'
        }]
      }
    },
    less: {
      app: {
        options: {
          yuicompress: true,
          concat: false
        },
        files: [{
          expand: true,
          cwd: 'src',
          src: ['**/*.less'],
          dest: 'app',
          ext: '.css'
        }]
      }
    },
    copy: {
      app: {
        files: []
      },
    },
    imagemin: {
      app: {
        options: {
          removeComments: true
        },
        files: [{
          expand: true,
          cwd: 'src',
          src: ['**/*.{png,jpg,jpeg}'],
          dest: 'app',
        }]
      }
    },
    concurrent: {
      build: ['coffee', 'less', 'copy', 'imagemin']
    },
    clean: {
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

  grunt.registerTask('default', ['concurrent:build', 'uglify', 'clean:post']);

};