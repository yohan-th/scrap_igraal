This service scrap [igraal.com](https://fr.igraal.com/) with android device to bypass security
1. `pip install -r requirementpy3.9.txt`
2. Save `192.x.x.x` IP and run WebDAV server to receive `./webdav/page.html` from android device
    - `nohup davserver -D ./webdav -J -H 0.0.0.0 -u yohan -p yohan &`
3. On android install [FF nightly](https://nightly.mozfr.org/) with [SingleFile](https://addons.mozilla.org/fr/firefox/addon/single-file/) + [Autosave](https://addons.mozilla.org/fr/firefox/addon/single-file-auto-save/)
4. Configurate `Destination` on Singlefile for WebDAV server
    - URL `http://[192.IP_SRV]:8008`
    - user `yohan`
    - pass `yohan`
5. Try to connect with `adb shell` and run `script.py` 
