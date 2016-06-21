
bundles: Gemfile
	bundle install --path bundles

serve: bundles
	bundle exec jekyll serve

