const babelify = require('babelify');
const browserify = require('browserify');
const concat = require('gulp-concat');
const gulp = require('gulp');
const sass = require('gulp-sass');
const source = require('vinyl-source-stream');
const jade = require('jade');
const gulpJade = require('gulp-jade');
const purge = require('gulp-css-purge');
const minify = require('gulp-clean-css');
const notifier = require('node-notifier');

gulp.task('build', function () {
    browserify('./src/lab3')
        .transform('babelify', {presets: ['env', 'react', 'stage-0']})
        .bundle()
        .on('error', function (err) {
            console.log(err.stack);
            notifier.notify({
                'title': 'Compile Error',
                'message': err.message
            });
            this.emit('end');
        })
        .pipe(source('lab3.js'))
        .pipe(gulp.dest('./dist/js'));

    gulp.src(['./src/**/*.sass', './src/**/*.scss'])
        .pipe(sass())
        .pipe(concat('styles-bundle.css'))
        .pipe(purge())
        .pipe(minify())
        .pipe(gulp.dest('./dist/css'));

    gulp.src('./src/*.jade')
        .pipe(gulpJade({
            jade: jade,
            pretty: true
        }))
        .pipe(gulp.dest('./dist'));
});