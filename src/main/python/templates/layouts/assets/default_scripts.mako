base_url = "${BASE}";
host = "${HOST}";
mount_point = "${MOUNT}";
None = undefined;

if (!String.prototype.format) {
  String.prototype.format = function(params) {
    if (!params)
        params = []
    str = this.replace();
    for (var i = 0; i < params.length; i++)
        str = str.replace("%s", params[i]);
    return str;
  };
}


function t(key, params, lang) {
    if (!params)
        params = [];
    if (!lang)
        lang = 'default';
    def = key.toLowerCase().replace("_"," ");
    languages = ${this.get_languages()};
    if (!languages)
        return def;
    if (lang == 'default') {
        conf = "${this.lang}";
        if (conf != "None" && conf)
            lang = conf;
        else if (languages['language'])
            lang = languages['language'];
    }
    language = languages[lang];
    if (!language) 
        return def;
    text = language[key] || def;
    return text.format(params)
}
