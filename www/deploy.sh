zip -r dist.zip dist

scp dist.zip thehog:~

ssh -t thehog 'unzip dist.zip; sudo cp -R dist/* /var/www/examon/; rm dist.zip; rm -r dist'
