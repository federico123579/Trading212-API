if [ "${DRIVER}" = "firefox" ]; then
    sleep 1

    wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
    mkdir geckodriver
    tar -xzf geckodriver-v0.18.0-linux64.tar.gz -C geckodriver
    mv ./geckodriver $HOME
    chmod +x $HOME/geckodriver/geckodriver

    curl "https://download.mozilla.org/?product=firefox-latest&lang=en-US&os=linux64" -L > firefox.tbz2
    bzip2 -dc firefox.tbz2 | tar xvf -
    mv ./firefox $HOME
    export PATH=$HOME/firefox:$PATH
    ls -lsa $HOME/geckodriver
    ls -lsa $HOME/firefox
    export PATH=$HOME/geckodriver:$PATH
fi

if [ "${DRIVER}" = "chrome" ]; then
    sleep 1

    FILE=`mktemp`; wget "http://chromedriver.storage.googleapis.com/2.30/chromedriver_linux64.zip" -qO $FILE && unzip $FILE chromedriver -d ~; rm $FILE; chmod 777 ~/chromedriver;
    export PATH=$HOME:$PATH
fi
