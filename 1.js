(function(a, b) {
    if (typeof define === "function" && define.amd) {
        define(["jquery"], b)
    } else {
        if (typeof exports === "object") {
            b(require("jquery"))
        } else {
            if (a.jQuery) {
                b(a.jQuery)
            } else {
                b(a.Zepto)
            }
        }
    }
}(this, function(e, f) {
    e.fn.jPlayer = function(j) {
        var i = "jPlayer";
        var g = typeof j === "string"
          , h = Array.prototype.slice.call(arguments, 1)
          , k = this;
        j = !g && h.length ? e.extend.apply(null, [true, j].concat(h)) : j;
        if (g && j.charAt(0) === "_") {
            return k
        }
        if (g) {
            this.each(function() {
                var l = e(this).data(i)
                  , m = l && e.isFunction(l[j]) ? l[j].apply(l, h) : l;
                if (m !== l && m !== f) {
                    k = m;
                    return false
                }
            })
        } else {
            this.each(function() {
                var l = e(this).data(i);
                if (l) {
                    l.option(j || {})
                } else {
                    e(this).data(i, new e.jPlayer(j,this))
                }
            })
        }
        return k
    }
    ;
    e.jPlayer = function(h, i) {
        if (arguments.length) {
            this.element = e(i);
            this.options = e.extend(true, {}, this.options, h);
            var g = this;
            this.element.bind("remove.jPlayer", function() {
                g.destroy()
            });
            this._init()
        }
    }
    ;
    e.jPlayer.emulateMethods = "load play pause";
    e.jPlayer.emulateStatus = "src readyState networkState currentTime duration paused ended playbackRate";
    e.jPlayer.emulateOptions = "muted volume";
    e.jPlayer.reservedEvent = "ready flashreset resize repeat error warning";
    e.jPlayer.event = {};
    e.each(["ready", "setmedia", "flashreset", "resize", "repeat", "click", "error", "warning", "loadstart", "progress", "suspend", "abort", "emptied", "stalled", "play", "pause", "loadedmetadata", "loadeddata", "waiting", "playing", "canplay", "canplaythrough", "seeking", "seeked", "timeupdate", "ended", "ratechange", "durationchange", "volumechange"], function() {
        e.jPlayer.event[this] = "jPlayer_" + this
    });
    e.jPlayer.htmlEvent = ["loadstart", "abort", "emptied", "stalled", "loadedmetadata", "canplay", "canplaythrough"];
    e.jPlayer.timeFormat = {
        showHour: false,
        showMin: true,
        showSec: true,
        padHour: false,
        padMin: true,
        padSec: true,
        sepHour: ":",
        sepMin: ":",
        sepSec: ""
    };
    var c = function() {
        this.init()
    };
    c.prototype = {
        init: function() {
            this.options = {
                timeFormat: e.jPlayer.timeFormat
            }
        },
        time: function(o) {
            o = (o && typeof o === "number") ? o : 0;
            var j = new Date(o * 1000)
              , h = j.getUTCHours()
              , i = this.options.timeFormat.showHour ? j.getUTCMinutes() : j.getUTCMinutes() + h * 60
              , k = this.options.timeFormat.showMin ? j.getUTCSeconds() : j.getUTCSeconds() + i * 60
              , n = (this.options.timeFormat.padHour && h < 10) ? "0" + h : h
              , m = (this.options.timeFormat.padMin && i < 10) ? "0" + i : i
              , g = (this.options.timeFormat.padSec && k < 10) ? "0" + k : k
              , l = "";
            l += this.options.timeFormat.showHour ? n + this.options.timeFormat.sepHour : "";
            l += this.options.timeFormat.showMin ? m + this.options.timeFormat.sepMin : "";
            l += this.options.timeFormat.showSec ? g + this.options.timeFormat.sepSec : "";
            return l
        }
    };
    var a = new c();
    e.jPlayer.convertTime = function(g) {
        return a.time(g)
    }
    ;
    e.jPlayer.uaBrowser = function(l) {
        var h = l.toLowerCase();
        var j = /(webkit)[ \/]([\w.]+)/;
        var m = /(opera)(?:.*version)?[ \/]([\w.]+)/;
        var i = /(msie) ([\w.]+)/;
        var k = /(mozilla)(?:.*? rv:([\w.]+))?/;
        var g = j.exec(h) || m.exec(h) || i.exec(h) || h.indexOf("compatible") < 0 && k.exec(h) || [];
        return {
            browser: g[1] || "",
            version: g[2] || "0"
        }
    }
    ;
    e.jPlayer.uaPlatform = function(m) {
        var j = m.toLowerCase();
        var n = /(ipad|iphone|ipod|android|blackberry|playbook|windows ce|webos)/;
        var l = /(ipad|playbook)/;
        var i = /(android)/;
        var k = /(mobile)/;
        var g = n.exec(j) || [];
        var h = l.exec(j) || !k.exec(j) && i.exec(j) || [];
        if (g[1]) {
            g[1] = g[1].replace(/\s/g, "_")
        }
        return {
            platform: g[1] || "",
            tablet: h[1] || ""
        }
    }
    ;
    e.jPlayer.browser = {};
    e.jPlayer.platform = {};
    var d = e.jPlayer.uaBrowser(navigator.userAgent);
    if (d.browser) {
        e.jPlayer.browser[d.browser] = true;
        e.jPlayer.browser.version = d.version
    }
    var b = e.jPlayer.uaPlatform(navigator.userAgent);
    if (b.platform) {
        e.jPlayer.platform[b.platform] = true;
        e.jPlayer.platform.mobile = !b.tablet;
        e.jPlayer.platform.tablet = !!b.tablet
    }
    e.jPlayer.focus = null;
    e.jPlayer.prototype = {
        count: 0,
        options: {
            solution: "html",
            preload: "metadata",
            volume: 0.8,
            supplied: "mp3",
            playbackRate: 1,
            defaultPlaybackRate: 1,
            cssSelector: {
                play: ".jp-play",
                pause: ".jp-pause",
                stop: ".jp-stop",
                seekBar: ".jp-seek-bar",
                playBar: ".jp-play-bar",
                volumeBar: ".jp-volume-bar",
                volumeBarValue: ".jp-volume-bar-value",
                volumeMax: ".jp-volume-max",
                currentTime: ".jp-current-time",
                duration: ".jp-duration",
                title: ".jp-title",
                playbackRateBar: ".jp-playback-rate-bar",
                playbackRateBarValue: ".jp-playback-rate-bar-value"
            },
            stateClass: {
                playing: "jp-state-playing",
                seeking: "jp-state-seeking",
                muted: "jp-state-muted",
                looped: "jp-state-looped",
                noVolume: "jp-state-no-volume"
            },
            idPrefix: "jp",
            errorAlerts: false,
            warningAlerts: false,
            smoothPlayBar: true,
            globalVolume: false
        },
        optionsAudio: {
            size: {
                width: "0px",
                height: "0px",
                cssClass: ""
            }
        },
        instances: {},
        status: {
            src: "",
            media: {},
            paused: true,
            format: {},
            formatType: "",
            waitForPlay: true,
            waitForLoad: true,
            srcSet: false,
            seekPercent: 0,
            currentPercentRelative: 0,
            currentPercentAbsolute: 0,
            currentTime: 0,
            duration: 0,
            remaining: 0,
            readyState: 0,
            networkState: 0,
            playbackRate: 1,
            ended: 0
        },
        internal: {
            ready: false
        },
        solution: {
            html: true
        },
        format: {
            mp3: {
                codec: "audio/mpeg",
                media: "audio"
            },
            m4a: {
                codec: 'audio/mp4; codecs="mp4a.40.2"',
                media: "audio"
            }
        },
        _init: function() {
            var g = this;
            this.element.empty();
            this.options.timeFormat = e.extend({}, e.jPlayer.timeFormat, this.options.timeFormat);
            this.internal.cmdsIgnored = e.jPlayer.platform.ipad || e.jPlayer.platform.iphone || e.jPlayer.platform.ipod;
            this.internal.domNode = this.element.get(0);
            this.androidFix = {
                setMedia: false,
                play: false,
                pause: false,
                time: NaN
            };
            if (e.jPlayer.platform.android) {
                this.options.preload = this.options.preload !== "auto" ? "metadata" : "auto"
            }
            this.formats = [];
            this.solutions = [];
            this.require = {};
            this.htmlElement = {};
            this.html = {};
            this.html.audio = {};
            this.css = {};
            this.css.cs = {};
            this.css.jq = {};
            this.ancestorJq = [];
            this.options.volume = this._limitValue(this.options.volume, 0, 1);
            e.each(this.options.supplied.toLowerCase().split(","), function(k, h) {
                var i = h.replace(/^\s+|\s+$/g, "");
                if (g.format[i]) {
                    var j = false;
                    e.each(g.formats, function(m, l) {
                        if (i === l) {
                            j = true;
                            return false
                        }
                    });
                    if (!j) {
                        g.formats.push(i)
                    }
                }
            });
            e.each(this.options.solution.toLowerCase().split(","), function(k, i) {
                var h = i.replace(/^\s+|\s+$/g, "");
                if (g.solution[h]) {
                    var j = false;
                    e.each(g.solutions, function(m, l) {
                        if (h === l) {
                            j = true;
                            return false
                        }
                    });
                    if (!j) {
                        g.solutions.push(h)
                    }
                }
            });
            this.internal.instance = "jp_" + this.count;
            this.instances[this.internal.instance] = this.element;
            if (!this.element.attr("id")) {
                this.element.attr("id", this.options.idPrefix + "_jplayer_" + this.count)
            }
            this.internal.self = e.extend({}, {
                id: this.element.attr("id"),
                jq: this.element
            });
            this.internal.audio = e.extend({}, {
                id: this.options.idPrefix + "_audio_" + this.count,
                jq: f
            });
            e.each(e.jPlayer.event, function(h, i) {
                if (g.options[h] !== f) {
                    g.element.bind(i + ".jPlayer", g.options[h]);
                    g.options[h] = f
                }
            });
            this.require.audio = false;
            e.each(this.formats, function(h, i) {
                g.require[g.format[i].media] = true
            });
            if (this.require.audio) {
                this.options = e.extend(true, {}, this.optionsAudio, this.options)
            }
            this._setSize();
            this.html.audio.available = false;
            if (this.require.audio) {
                this.htmlElement.iframe = document.createElement("iframe");
                this.htmlElement.iframe.style.width = "0px";
                this.htmlElement.iframe.style.height = "0px";
                this.htmlElement.iframe.style.visibility = "hidden";
                this.htmlElement.iframe.style.display = "none";
                this.element.append(this.htmlElement.iframe);
                this.htmlElement.iframe.contentWindow.document.head.innerHTML = '<meta charset="UTF-8">\n<meta name="referrer" content="no-referrer">';
                this.htmlElement.audio = this.htmlElement.iframe.contentWindow.document.createElement("audio");
                this.htmlElement.audio.id = this.internal.audio.id;
                this.html.audio.available = !!this.htmlElement.audio.canPlayType && this._testCanPlayType(this.htmlElement.audio)
            }
            this.html.canPlay = {};
            e.each(this.formats, function(h, i) {
                g.html.canPlay[i] = g.html[g.format[i].media].available && "" !== g.htmlElement[g.format[i].media].canPlayType(g.format[i].codec)
            });
            this.html.desired = false;
            e.each(this.solutions, function(i, h) {
                if (i === 0) {
                    g[h].desired = true
                } else {
                    var j = false;
                    e.each(g.formats, function(k, l) {
                        if (g[g.solutions[0]].canPlay[l]) {
                            if (g.format[l].media === "audio") {
                                j = true
                            }
                        }
                    });
                    g[h].desired = (g.require.audio && !j)
                }
            });
            this.html.support = {};
            e.each(this.formats, function(h, i) {
                g.html.support[i] = g.html.canPlay[i] && g.html.desired
            });
            this.html.used = false;
            e.each(this.solutions, function(i, h) {
                e.each(g.formats, function(j, k) {
                    if (g[h].support[k]) {
                        g[h].used = true;
                        return false
                    }
                })
            });
            this._resetActive();
            this._resetGate();
            this._cssSelectorAncestor(this.options.cssSelectorAncestor);
            if (this.html.used) {
                this.status.playbackRateEnabled = this._testPlaybackRate("audio")
            } else {
                this.status.playbackRateEnabled = false
            }
            this._updatePlaybackRate();
            if (this.html.used) {
                if (this.html.audio.available) {
                    this._addHtmlEventListeners(this.htmlElement.audio, this.html.audio);
                    this.internal.audio.jq = e("#" + this.internal.audio.id)
                }
            }
            if (this.html.used) {
                setTimeout(function() {
                    g.internal.ready = true;
                    g._trigger(e.jPlayer.event.repeat);
                    g._trigger(e.jPlayer.event.ready)
                }, 100)
            }
        },
        _addHtmlEventListeners: function(g, i) {
            var h = this;
            g.preload = this.options.preload;
            g.muted = this.options.muted;
            g.volume = this.options.volume;
            if (this.status.playbackRateEnabled) {
                g.defaultPlaybackRate = this.options.defaultPlaybackRate;
                g.playbackRate = this.options.playbackRate
            }
            g.addEventListener("progress", function() {
                if (i.gate) {
                    if (h.internal.cmdsIgnored && this.readyState > 0) {
                        h.internal.cmdsIgnored = false
                    }
                    h._getHtmlStatus(g);
                    h._updateInterface();
                    h._trigger(e.jPlayer.event.progress)
                }
            }, false);
            g.addEventListener("loadeddata", function() {
                if (i.gate) {
                    h.androidFix.setMedia = false;
                    if (h.androidFix.play) {
                        h.androidFix.play = false;
                        h.play(h.androidFix.time)
                    }
                    if (h.androidFix.pause) {
                        h.androidFix.pause = false;
                        h.pause(h.androidFix.time)
                    }
                    h._trigger(e.jPlayer.event.loadeddata)
                }
            }, false);
            g.addEventListener("timeupdate", function() {
                if (i.gate) {
                    h._getHtmlStatus(g);
                    h._updateInterface();
                    h._trigger(e.jPlayer.event.timeupdate)
                }
            }, false);
            g.addEventListener("durationchange", function() {
                if (i.gate) {
                    h._getHtmlStatus(g);
                    h._updateInterface();
                    h._trigger(e.jPlayer.event.durationchange)
                }
            }, false);
            g.addEventListener("play", function() {
                if (i.gate) {
                    h._updateButtons(true);
                    h._trigger(e.jPlayer.event.play)
                }
            }, false);
            g.addEventListener("playing", function() {
                if (i.gate) {
                    h._updateButtons(true);
                    h._seeked();
                    h._trigger(e.jPlayer.event.playing)
                }
            }, false);
            g.addEventListener("pause", function() {
                if (i.gate) {
                    h._updateButtons(false);
                    h._trigger(e.jPlayer.event.pause)
                }
            }, false);
            g.addEventListener("waiting", function() {
                if (i.gate) {
                    h._seeking();
                    h._trigger(e.jPlayer.event.waiting);
                }
            }, false);
            g.addEventListener("seeked", function() {
                if (i.gate) {
                    h._seeked();
                    h._trigger(e.jPlayer.event.seeked)
                }
            }, false);
            g.addEventListener("volumechange", function() {
                if (i.gate) {
                    h.options.volume = g.volume;
                    h.options.muted = g.muted;
                    h._updateMute();
                    h._updateVolume();
                    h._trigger(e.jPlayer.event.volumechange)
                }
            }, false);
            g.addEventListener("ratechange", function() {
                if (i.gate) {
                    h.options.defaultPlaybackRate = g.defaultPlaybackRate;
                    h.options.playbackRate = g.playbackRate;
                    h._updatePlaybackRate();
                    h._trigger(e.jPlayer.event.ratechange)
                }
            }, false);
            g.addEventListener("suspend", function() {
                if (i.gate) {
                    h._seeked();
                    h._trigger(e.jPlayer.event.suspend)
                }
            }, false);
            g.addEventListener("ended", function() {
                if (i.gate) {
                    if (!e.jPlayer.browser.webkit) {
                        h.htmlElement.media.currentTime = 0
                    }
                    h.htmlElement.media.pause();
                    h._updateButtons(false);
                    h._getHtmlStatus(g, true);
                    h._updateInterface();
                    h._trigger(e.jPlayer.event.ended)
                }
            }, false);
            g.addEventListener("error", function() {
                if (i.gate) {
                    h._updateButtons(false);
                    h._seeked();
                    if (h.status.srcSet) {
                        clearTimeout(h.internal.htmlDlyCmdId);
                        h.status.waitForLoad = true;
                        h.status.waitForPlay = true;
                        h._error({
                            type: e.jPlayer.error.URL,
                            context: h.status.src,
                            message: e.jPlayer.errorMsg.URL,
                            hint: e.jPlayer.errorHint.URL
                        })
                    }
                }
            }, false);
            e.each(e.jPlayer.htmlEvent, function(k, j) {
                g.addEventListener(this, function() {
                    if (i.gate) {
                        h._trigger(e.jPlayer.event[j])
                    }
                }, false)
            })
        },
        _getHtmlStatus: function(k, h) {
            var g = 0
              , i = 0
              , j = 0
              , l = 0;
            if (isFinite(k.duration)) {
                this.status.duration = k.duration
            }
            g = k.currentTime;
            i = (this.status.duration > 0) ? 100 * g / this.status.duration : 0;
            if ((typeof k.seekable === "object") && (k.seekable.length > 0)) {
                j = (this.status.duration > 0) ? 100 * k.seekable.end(k.seekable.length - 1) / this.status.duration : 100;
                l = (this.status.duration > 0) ? 100 * k.currentTime / k.seekable.end(k.seekable.length - 1) : 0
            } else {
                j = 100;
                l = i
            }
            if (h) {
                g = 0;
                l = 0;
                i = 0
            }
            this.status.seekPercent = j;
            this.status.currentPercentRelative = l;
            this.status.currentPercentAbsolute = i;
            this.status.currentTime = g;
            this.status.remaining = this.status.duration - this.status.currentTime;
            this.status.readyState = k.readyState;
            this.status.networkState = k.networkState;
            this.status.playbackRate = k.playbackRate;
            this.status.ended = k.ended
        },
        _updateInterface: function() {
            if (this.css.jq.seekBar.length) {
                this.css.jq.seekBar.width(this.status.seekPercent + "%")
            }
            if (this.css.jq.playBar.length) {
                if (this.options.smoothPlayBar) {
                    this.css.jq.playBar.stop().animate({
                        width: this.status.currentPercentAbsolute + "%"
                    }, 250, "linear")
                } else {
                    this.css.jq.playBar.width(this.status.currentPercentRelative + "%")
                }
            }
            var i = "";
            if (this.css.jq.currentTime.length) {
                i = this._convertTime(this.status.currentTime);
                if (i !== this.css.jq.currentTime.text()) {
                    this.css.jq.currentTime.text(this._convertTime(this.status.currentTime))
                }
            }
            var g = ""
              , j = this.status.duration
              , h = this.status.remaining;
            if (this.css.jq.duration.length) {
                if (typeof this.status.media.duration === "string") {
                    g = this.status.media.duration
                } else {
                    if (typeof this.status.media.duration === "number") {
                        j = this.status.media.duration;
                        h = j - this.status.currentTime
                    }
                    if (this.options.remainingDuration) {
                        g = (h > 0 ? "-" : "") + this._convertTime(h)
                    } else {
                        g = this._convertTime(j)
                    }
                }
                if (g !== this.css.jq.duration.text()) {
                    this.css.jq.duration.text(g)
                }
            }
        },
        _updateButtons: function(g) {
            if (g === f) {
                g = !this.status.paused
            } else {
                this.status.paused = !g
            }
            if (this.css.jq.play.length && this.css.jq.pause.length) {
                if (g) {
                    this.css.jq.play.hide();
                    this.css.jq.pause.show()
                } else {
                    this.css.jq.play.show();
                    this.css.jq.pause.hide()
                }
            }
        },
        _updatePlaybackRate: function() {
            var h = this.options.playbackRate
              , g = (h - this.options.minPlaybackRate) / (this.options.maxPlaybackRate - this.options.minPlaybackRate);
            if (this.status.playbackRateEnabled) {
                if (this.css.jq.playbackRateBar.length) {
                    this.css.jq.playbackRateBar.show()
                }
                if (this.css.jq.playbackRateBarValue.length) {
                    this.css.jq.playbackRateBarValue.show();
                    this.css.jq.playbackRateBarValue[this.options.verticalPlaybackRate ? "height" : "width"]((g * 100) + "%")
                }
            } else {
                if (this.css.jq.playbackRateBar.length) {
                    this.css.jq.playbackRateBar.hide()
                }
                if (this.css.jq.playbackRateBarValue.length) {
                    this.css.jq.playbackRateBarValue.hide()
                }
            }
        },
        _updateVolume: function(g) {
            if (g === f) {
                g = this.options.volume
            }
            g = this.options.muted ? 0 : g;
            if (this.status.noVolume) {
                this.addStateClass("noVolume");
                if (this.css.jq.volumeBar.length) {
                    this.css.jq.volumeBar.hide()
                }
                if (this.css.jq.volumeBarValue.length) {
                    this.css.jq.volumeBarValue.hide()
                }
                if (this.css.jq.volumeMax.length) {
                    this.css.jq.volumeMax.hide()
                }
            } else {
                this.removeStateClass("noVolume");
                if (this.css.jq.volumeBar.length) {
                    this.css.jq.volumeBar.show()
                }
                if (this.css.jq.volumeBarValue.length) {
                    this.css.jq.volumeBarValue.show();
                    this.css.jq.volumeBarValue[this.options.verticalVolume ? "height" : "width"]((g * 100) + "%")
                }
                if (this.css.jq.volumeMax.length) {
                    this.css.jq.volumeMax.show()
                }
            }
        },
        _updateMute: function(g) {
            if (g === f) {
                g = this.options.muted
            }
            if (g) {
                this.addStateClass("muted")
            } else {
                this.removeStateClass("muted")
            }
            if (this.css.jq.mute.length && this.css.jq.unmute.length) {
                if (this.status.noVolume) {
                    this.css.jq.mute.hide();
                    this.css.jq.unmute.hide()
                } else {
                    if (g) {
                        this.css.jq.mute.hide();
                        this.css.jq.unmute.show()
                    } else {
                        this.css.jq.mute.show();
                        this.css.jq.unmute.hide();
                    }
                }
            }
        },
        _seeking: function() {
            if (this.css.jq.seekBar.length) {
                this.css.jq.seekBar.addClass("jp-seeking-bg")
            }
            this.addStateClass("seeking")
        },
        _seeked: function() {
            if (this.css.jq.seekBar.length) {
                this.css.jq.seekBar.removeClass("jp-seeking-bg")
            }
            this.removeStateClass("seeking")
        },
        _convertTime: c.prototype.time,
        _muted: function(g) {
            this.mutedWorker(g);
            if (this.options.globalVolume) {
                this.tellOthers("mutedWorker", function() {
                    return this.options.globalVolume
                }, g)
            }
        },
        mute: function(h) {
            var g = typeof h === "object";
            if (g && this.options.useStateClassSkin && this.options.muted) {
                this._muted(false)
            } else {
                h = h === f ? true : !!h;
                this._muted(h)
            }
        },
        unmute: function(g) {
            g = g === f ? true : !!g;
            this._muted(!g)
        },
        volumeMax: function() {
            this.volume(1)
        },
        _limitValue: function(i, h, g) {
            return (i < h) ? h : ((i > g) ? g : i)
        },
        _validString: function(g) {
            return (g && typeof g === "string")
        },
        _setSize: function() {
            this.status.width = this.options.size.width;
            this.status.height = this.options.size.height;
            this.status.cssClass = this.options.size.cssClass;
            this.element.css({
                "width": this.status.width,
                "height": this.status.height
            })
        },
        _cssSelectorAncestor: function(h) {
            var g = this;
            this.options.cssSelectorAncestor = h;
            this.ancestorJq = h ? e(h) : [];
            if (h && this.ancestorJq.length !== 1) {
                this._warning({
                    type: e.jPlayer.warning.CSS_SELECTOR_COUNT,
                    context: h,
                    message: e.jPlayer.warningMsg.CSS_SELECTOR_COUNT + this.ancestorJq.length + " found for cssSelectorAncestor.",
                    hint: e.jPlayer.warningHint.CSS_SELECTOR_COUNT
                })
            }
            e.each(this.options.cssSelector, function(i, j) {
                g._cssSelector(i, j)
            });
            this._updateButtons()
        },
        _cssSelector: function(i, j) {
            var g = this;
            if (typeof j === "string") {
                if (e.jPlayer.prototype.options.cssSelector[i]) {
                    if (this.css.jq[i] && this.css.jq[i].length) {
                        this.css.jq[i].unbind(".jPlayer")
                    }
                    this.options.cssSelector[i] = j;
                    this.css.cs[i] = this.options.cssSelectorAncestor + " " + j;
                    if (j) {
                        this.css.jq[i] = e(this.css.cs[i])
                    } else {
                        this.css.jq[i] = []
                    }
                    if (this.css.jq[i].length && this[i]) {
                        var h = function(k) {
                            k.preventDefault();
                            g[i](k);
                            if (g.options.autoBlur) {
                                e(this).blur()
                            } else {
                                e(this).focus()
                            }
                        };
                        this.css.jq[i].bind("click.jPlayer", h)
                    }
                    if (j && this.css.jq[i].length !== 1) {
                        this._warning({
                            type: e.jPlayer.warning.CSS_SELECTOR_COUNT,
                            context: this.css.cs[i],
                            message: e.jPlayer.warningMsg.CSS_SELECTOR_COUNT + this.css.jq[i].length + " found for " + i + " method.",
                            hint: e.jPlayer.warningHint.CSS_SELECTOR_COUNT
                        })
                    }
                } else {
                    this._warning({
                        type: e.jPlayer.warning.CSS_SELECTOR_METHOD,
                        context: i,
                        message: e.jPlayer.warningMsg.CSS_SELECTOR_METHOD,
                        hint: e.jPlayer.warningHint.CSS_SELECTOR_METHOD
                    })
                }
            } else {
                this._warning({
                    type: e.jPlayer.warning.CSS_SELECTOR_STRING,
                    context: j,
                    message: e.jPlayer.warningMsg.CSS_SELECTOR_STRING,
                    hint: e.jPlayer.warningHint.CSS_SELECTOR_STRING
                })
            }
        },
        _testCanPlayType: function(h) {
            try {
                h.canPlayType(this.format.mp3.codec);
                return true
            } catch (g) {
                return false
            }
        },
        _testPlaybackRate: function(i) {
            var h, g = 0.5;
            i = typeof i === "string" ? i : "audio";
            h = document.createElement(i);
            try {
                if ("playbackRate"in h) {
                    h.playbackRate = g;
                    return h.playbackRate === g
                } else {
                    return false
                }
            } catch (j) {
                return false
            }
        },
        _absoluteMediaUrls: function(h) {
            var g = this;
            e.each(h, function(j, i) {
                if (i && g.format[j] && i.substr(0, 5) !== "data:") {
                    h[j] = g._qualifyURL(i)
                }
            });
            return h
        },
        _qualifyURL: function(g) {
            var h = document.createElement("div");
            h.innerHTML = '<a href="' + this._escapeHtml(g) + '">x</a>';
            return h.firstChild.href
        },
        _escapeHtml: function(g) {
            return g.split("&").join("&amp;").split("<").join("&lt;").split(">").join("&gt;").split('"').join("&quot;")
        },
        _resetMedia: function() {
            this._resetStatus();
            this._updateButtons(false);
            this._updateInterface();
            this._seeked();
            clearTimeout(this.internal.htmlDlyCmdId);
            if (this.html.active) {
                this._html_resetMedia()
            }
        },
        _resetStatus: function() {
            this.status = e.extend({}, this.status, e.jPlayer.prototype.status)
        },
        _resetGate: function() {
            this.html.audio.gate = false
        },
        _resetActive: function() {
            this.html.active = false
        },
        removeStateClass: function(g) {
            if (this.ancestorJq.length) {
                this.ancestorJq.removeClass(this.options.stateClass[g])
            }
        },
        setMedia: function(i) {
            var h = this
              , g = false;
            this._resetMedia();
            this._resetGate();
            this._resetActive();
            this.androidFix.setMedia = false;
            this.androidFix.play = false;
            this.androidFix.pause = false;
            i = this._absoluteMediaUrls(i);
            e.each(this.formats, function(j, k) {
                e.each(h.solutions, function(m, l) {
                    if (h[l].support[k] && h._validString(i[k])) {
                        var n = l === "html";
                        if (n) {
                            h.html.audio.gate = true;
                            h._html_setAudio(i);
                            h.html.active = true;
                            if (e.jPlayer.platform.android) {
                                h.androidFix.setMedia = true
                            }
                        }
                        g = true;
                        return false
                    }
                });
                if (g) {
                    return false
                }
            });
            if (g) {
                if (typeof i.title === "string") {
                    if (this.css.jq.title.length) {
                        this.css.jq.title.html(i.title)
                    }
                    if (this.htmlElement.audio) {
                        this.htmlElement.audio.setAttribute("title", i.title)
                    }
                }
                this.status.srcSet = true;
                this.status.media = e.extend({}, i);
                this._updateButtons(false);
                this._updateInterface();
                this._trigger(e.jPlayer.event.setmedia)
            } else {
                this._error({
                    type: e.jPlayer.error.NO_SUPPORT,
                    context: "{supplied:'" + this.options.supplied + "'}",
                    message: e.jPlayer.errorMsg.NO_SUPPORT,
                    hint: e.jPlayer.errorHint.NO_SUPPORT
                })
            }
        },
        load: function() {
            if (this.status.srcSet) {
                if (this.html.active) {
                    this._html_load()
                }
            } else {
                this._urlNotSetError("load")
            }
        },
        play: function(h) {
            var g = typeof h === "object";
            if (g && this.options.useStateClassSkin && !this.status.paused) {
                this.pause(h)
            } else {
                h = (typeof h === "number") ? h : NaN;
                if (this.status.srcSet) {
                    if (this.html.active) {
                        this._html_play(h)
                    }
                } else {
                    this._urlNotSetError("play")
                }
            }
        },
        pause: function(g) {
            g = (typeof g === "number") ? g : NaN;
            if (this.status.srcSet) {
                if (this.html.active) {
                    this._html_pause(g)
                }
            } else {
                this._urlNotSetError("pause")
            }
        },
        stop: function() {
            if (this.status.srcSet) {
                if (this.html.active) {
                    this._html_pause(0)
                }
            } else {
                this._urlNotSetError("stop")
            }
        },
        playHead: function(g) {
            g = this._limitValue(g, 0, 100);
            if (this.status.srcSet) {
                if (this.html.active) {
                    this._html_playHead(g)
                }
            } else {
                this._urlNotSetError("playHead")
            }
        },
        playbackRate: function(g) {
            this._setOption("playbackRate", g)
        },
        playbackRateBar: function(l) {
            if (this.css.jq.playbackRateBar.length) {
                var g = e(l.currentTarget), j = g.offset(), o = l.pageX - j.left, p = g.width(), n = g.height() - l.pageY + j.top, k = g.height(), m, i;
                if (this.options.verticalPlaybackRate) {
                    m = n / k
                } else {
                    m = o / p
                }
                i = m * (this.options.maxPlaybackRate - this.options.minPlaybackRate) + this.options.minPlaybackRate;
                this.playbackRate(i)
            }
        },
        addStateClass: function(g) {
            if (this.ancestorJq.length) {
                this.ancestorJq.addClass(this.options.stateClass[g])
            }
        },
        _html_setFormat: function(h) {
            var g = this;
            e.each(this.formats, function(i, j) {
                if (g.html.support[j] && h[j]) {
                    g.status.src = h[j];
                    g.status.format[j] = true;
                    g.status.formatType = j;
                    return false
                }
            })
        },
        _html_setAudio: function(g) {
            this._html_setFormat(g);
            this.htmlElement.media = this.htmlElement.audio;
            this._html_initMedia(g)
        },
        _html_initMedia: function(g) {
            this.htmlElement.media.src = this.status.src;
            if (this.options.preload !== "none") {
                this._html_load()
            }
            this._trigger(e.jPlayer.event.timeupdate)
        },
        _html_resetMedia: function() {
            if (this.htmlElement.media) {
                this.htmlElement.media.pause()
            }
        },
        _html_setProperty: function(h, g) {
            if (this.html.audio.available) {
                this.htmlElement.audio[h] = g
            }
        },
        _html_checkWaitForPlay: function() {
            if (this.status.waitForPlay) {
                this.status.waitForPlay = false
            }
        },
        _html_load: function() {
            if (this.status.waitForLoad) {
                this.status.waitForLoad = false;
                this.htmlElement.media.load()
            }
            clearTimeout(this.internal.htmlDlyCmdId)
        },
        _html_play: function(j) {
            var g = this
              , i = this.htmlElement.media;
            this.androidFix.pause = false;
            this._html_load();
            if (this.androidFix.setMedia) {
                this.androidFix.play = true;
                this.androidFix.time = j
            } else {
                if (!isNaN(j)) {
                    if (this.internal.cmdsIgnored) {
                        i.play()
                    }
                    try {
                        if (!i.seekable || typeof i.seekable === "object" && i.seekable.length > 0) {
                            i.currentTime = j;
                            i.play()
                        } else {
                            throw 1
                        }
                    } catch (h) {
                        this.internal.htmlDlyCmdId = setTimeout(function() {
                            g.play(j)
                        }, 250);
                        return
                    }
                } else {
                    i.play()
                }
            }
            this._html_checkWaitForPlay()
        },
        _html_pause: function(j) {
            var g = this
              , i = this.htmlElement.media;
            this.androidFix.play = false;
            if (j > 0) {
                this._html_load()
            } else {
                clearTimeout(this.internal.htmlDlyCmdId)
            }
            i.pause();
            if (this.androidFix.setMedia) {
                this.androidFix.pause = true;
                this.androidFix.time = j
            } else {
                if (!isNaN(j)) {
                    try {
                        if (!i.seekable || typeof i.seekable === "object" && i.seekable.length > 0) {
                            i.currentTime = j
                        } else {
                            throw 1
                        }
                    } catch (h) {
                        this.internal.htmlDlyCmdId = setTimeout(function() {
                            g.pause(j)
                        }, 250);
                        return
                    }
                }
            }
            if (j > 0) {
                this._html_checkWaitForPlay()
            }
        },
        _html_playHead: function(i) {
            var g = this
              , j = this.htmlElement.media;
            this._html_load();
            try {
                if (typeof j.seekable === "object" && j.seekable.length > 0) {
                    j.currentTime = i * j.seekable.end(j.seekable.length - 1) / 100
                } else {
                    if (j.duration > 0 && !isNaN(j.duration)) {
                        j.currentTime = i * j.duration / 100
                    } else {
                        throw "e"
                    }
                }
            } catch (h) {
                this.internal.htmlDlyCmdId = setTimeout(function() {
                    g.playHead(i)
                }, 250);
                return
            }
            if (!this.status.waitForLoad) {
                this._html_checkWaitForPlay()
            }
        },
        _trigger: function(h, g, i) {
            var j = e.Event(h);
            j.jPlayer = {};
            j.jPlayer.options = e.extend(true, {}, this.options);
            j.jPlayer.status = e.extend(true, {}, this.status);
            j.jPlayer.html = e.extend(true, {}, this.html);
            if (g) {
                j.jPlayer.error = e.extend({}, g)
            }
            if (i) {
                j.jPlayer.warning = e.extend({}, i)
            }
            this.element.trigger(j)
        },
        _error: function(g) {
            this._trigger(e.jPlayer.event.error, g);
            if (this.options.errorAlerts) {
                this._alert("Error!" + (g.message ? "\n" + g.message : "") + (g.hint ? "\n" + g.hint : "") + "\nContext: " + g.context)
            }
        },
        _warning: function(g) {
            this._trigger(e.jPlayer.event.warning, f, g);
            if (this.options.warningAlerts) {
                this._alert("Warning!" + (g.message ? "\n" + g.message : "") + (g.hint ? "\n" + g.hint : "") + "\nContext: " + g.context)
            }
        },
        _urlNotSetError: function(g) {
            this._error({
                type: e.jPlayer.error.URL_NOT_SET,
                context: g,
                message: e.jPlayer.errorMsg.URL_NOT_SET,
                hint: e.jPlayer.errorHint.URL_NOT_SET
            })
        },
        _setOption: function(h, i) {
            var g = this;
            switch (h) {
            case "volume":
                this.volume(i);
                break;
            case "muted":
                this._muted(i);
                break;
            case "globalVolume":
                this.options[h] = i;
                break;
            case "cssSelectorAncestor":
                this._cssSelectorAncestor(i);
                break;
            case "cssSelector":
                e.each(i, function(j, k) {
                    g._cssSelector(j, k)
                });
                break;
            case "playbackRate":
                this.options[h] = i = this._limitValue(i, this.options.minPlaybackRate, this.options.maxPlaybackRate);
                if (this.html.used) {
                    this._html_setProperty("playbackRate", i)
                }
                this._updatePlaybackRate();
                break;
            case "defaultPlaybackRate":
                this.options[h] = i = this._limitValue(i, this.options.minPlaybackRate, this.options.maxPlaybackRate);
                if (this.html.used) {
                    this._html_setProperty("defaultPlaybackRate", i)
                }
                this._updatePlaybackRate();
                break;
            case "minPlaybackRate":
                this.options[h] = i = this._limitValue(i, 0.1, this.options.maxPlaybackRate - 0.1);
                this._updatePlaybackRate();
                break;
            case "maxPlaybackRate":
                this.options[h] = i = this._limitValue(i, this.options.minPlaybackRate + 0.1, 16);
                this._updatePlaybackRate();
                break;
            case "loop":
                this._loop(i);
                break;
            case "remainingDuration":
                this.options[h] = i;
                this._updateInterface();
                break;
            case "toggleDuration":
                this.options[h] = i;
                break;
            case "noVolume":
                this.options[h] = e.extend({}, this.options[h], i);
                this.status.noVolume = this._uaBlocklist(this.options.noVolume);
                this._updateVolume();
                this._updateMute();
                break;
            case "timeFormat":
                this.options[h] = e.extend({}, this.options[h], i);
                break
            }
            return this
        },
        destroy: function() {
            this.clearMedia();
            if (this.css.jq.currentTime.length) {
                this.css.jq.currentTime.text("")
            }
            if (this.css.jq.duration.length) {
                this.css.jq.duration.text("")
            }
            e.each(this.css.jq, function(g, h) {
                if (h.length) {
                    h.unbind(".jPlayer")
                }
            });
            if (this === e.jPlayer.focus) {
                e.jPlayer.focus = null
            }
            this.element.removeData("jPlayer");
            this.element.unbind(".jPlayer");
            this.element.empty();
            delete this.instances[this.internal.instance]
        },
        destroyRemoved: function() {
            var g = this;
            e.each(this.instances, function(j, h) {
                if (g.element !== h) {
                    if (!h.data("jPlayer")) {
                        h.jPlayer("destroy");
                        delete g.instances[j]
                    }
                }
            })
        },
        tellOthers: function(k, j) {
            var h = this
              , g = typeof j === "function"
              , i = Array.prototype.slice.call(arguments);
            if (typeof k !== "string") {
                return
            }
            if (g) {
                i.splice(1, 1)
            }
            e.jPlayer.prototype.destroyRemoved();
            e.each(this.instances, function() {
                if (h.element !== this) {
                    if (!g || j.call(this.data("jPlayer"), h)) {
                        this.jPlayer.apply(this, i)
                    }
                }
            })
        }
    };
    e.jPlayer.error = {
        NO_SOLUTION: "e_no_solution",
        NO_SUPPORT: "e_no_support",
        URL: "e_url",
        URL_NOT_SET: "e_url_not_set",
        VERSION: "e_version"
    };
    e.jPlayer.errorMsg = {
        NO_SOLUTION: "No solution can be found by jPlayer in this browser. Neither HTML nor Flash can be used.",
        NO_SUPPORT: "It is not possible to play any media format provided in setMedia() on this browser using your current options.",
        URL: "Media URL could not be loaded.",
        URL_NOT_SET: "Attempt to issue media playback commands, while no media url is set.",
        VERSION: "123123"
    };
    e.jPlayer.errorHint = {
        NO_SOLUTION: "Review the jPlayer options: support and supplied.",
        NO_SUPPORT: "Video or audio formats defined in the supplied option are missing.",
        URL: "Check media URL is valid.",
        URL_NOT_SET: "Use setMedia() to set the media URL.",
        VERSION: "Update jPlayer files."
    };
    e.jPlayer.warning = {
        CSS_SELECTOR_COUNT: "e_css_selector_count",
        CSS_SELECTOR_METHOD: "e_css_selector_method",
        CSS_SELECTOR_STRING: "e_css_selector_string",
        OPTION_KEY: "e_option_key"
    };
    e.jPlayer.warningMsg = {
        CSS_SELECTOR_COUNT: "The number of css selectors found did not equal one: ",
        CSS_SELECTOR_METHOD: "The methodName given in jPlayer('cssSelector') is not a valid jPlayer method.",
        CSS_SELECTOR_STRING: "The methodCssSelector given in jPlayer('cssSelector') is not a String or is empty.",
        OPTION_KEY: "The option requested in jPlayer('option') is undefined."
    };
    e.jPlayer.warningHint = {
        CSS_SELECTOR_COUNT: "Check your css selector and the ancestor.",
        CSS_SELECTOR_METHOD: "Check your method name.",
        CSS_SELECTOR_STRING: "Check your css selector is a string.",
        OPTION_KEY: "Check your option name."
    }
}));
var iｉl = 'jsjiami.com.v6'
  , i1l1i = [iｉl, 'OsOJwowfw6PCiQ==', 'Z8Ogwoodwp9f', 'LgXCukI=', 'wqjDoRDCoMOc', 'TRfCs8ODwrcr', 'PcOBNQXDgXk=', 'wrLChcK+axN4LMKdwrs=', 'w7jCgcOXw7kjGxXCjjw=', 'w6DCk8OGw6gK', 'w53DqlMQJks=', 'VzNF', 'wr9VP2F2', 'w5DDtmo1Mw==', 'IsKrKMO9wqNX', 'IsKTw5Uzw6F5', 'wqBJbFtrKg==', 'w5zCuQN0a8On', 'w7nDpFt0M8OH', 'J03CjCQ=', 'w4PDvFNpPw==', 'CsOmDsO6w7rCpw==', 'NMKFwroPw4LClA==', 'w6HCncOV', 'dhJXw6w=', 'OsO5w7/Dr17DsljCllXDv2bCsHvDhwDDq18NJVAtEiA=', 'OjXCgh4=', 'woM9J8KfccOsZRRK', 'w7/Cl8K4ZxF9', 'OygKXMOqWQ==', '5Z+C57mV5pa05ZGiGGpCR8Kd5ZOO5LmU572c', 'O3LDj0/Cig==', 'w5nDtH8/', 'fHXDmVbCnMOCw73DoA==', 'wpbCrhQ=', 'wqlAEsKydcKf', 'UWk0w4ZtRQ==', 'B8KpRQ==', 'w6XChsOGw7sRRl/DjyvDuUHCmSvCkcK9ESfCq8Kuw4vClxYEXsO1wrDCqFHDmcKywowWGsKa', 'wqYYF8K7JA==', 'woDChjs=', 'KcKAwqIqw4s=', 'TMOmwok/woZkw54=', 'OmPDm8Ok', 'wpk1JMKd', 'woLCncOp', 'Kg3CrVM=', 'JcOmJg0=', 'wq/CmyI=', 'EMO1Jg==', 'ZzgjFBU=', 'DcOLwpsrwrNu', 'wqjDpDXCoMKEw7Q=', 'QsOlwoo9wpp/', 'w4jCk2vDoQ==', 'w4TCnsOew4JTTQ==', 'wokYF8KyUMK6', 'wrEvRlbCjcO6', 'fCFkal/DpA==', 'DcKHw6zDmg==', 'wqwQCMKq', 'wptlJcKUW8Oo', 'eBZGw7A=', 'TlxrwqnCv8On', 'w4nDjHXDksOreg==', 'YsK6Jw==', 'EnU0w45d', 'EMOgw73DpUPCqg==', 'aMOzLBx6', 'FsKiaUJ4w6nDuDw=', 'BcK6wqnDhMKOw4w=', 'M2XDh8KQX38=', 'OcKAwqUnw4zCscO7fg==', 'J8OqFxVg', 'G8KqYWh9wrk=', 'LcOqMhw=', 'RDDDoQ==', 'O8ODwpYJwrU=', 'w4TDp2FpKMOHHEQ=', 'wr/CnsOkdg==', 'dj80', 'aH3DmETCmw==', 'wpHCvQhYw4xaMEzCogvDkcK2V8OPwojCkQ==', 'wrnCisKr', 'Q8OvwoPCtg==', 'AcOgJHrDvw==', 'w6LDhDfDvsOsJw==', 'AMKaw5HDgcKL', 'GcOiw7I=', 'SCpAcRo=', 'wrrCgC0P', 'IsOrw5UWwrlc', 'wobDm8OuB1EO', 'QcOzcCIjw7Q=', 'KcKlXcO2w74f', 'PcKcNQDDoSQ=', 'KcKFAMO2w5sf', 'IcKoVQ==', 'wrYwLQ==', 'w6TCnMOWw64aIwPChTzCnnE=', 'w5zDpF50M8On', 'J8OOwogTwrl8', 'AsOqMjBldQ==', 'w7jDr3YQI24=', 'R8K4wo9lwron', 'wr7Cg8OMIy0=', 'wp/Drm40', 'JsOSwp8Iw7zDlkNdbB3DpDTCu8OIw5HCi31xwrRZFlFVAMKEwqTDmmvDpw3CrQ==', 'IsOOwr5/w4c=', 'Hg0q', 'FcK9w5jDhUY=', 'wpQvRlbCqMKi', 'wpDDiiN2bgI=', 'UsOVAMKTT1Mc', 'ZMKrVQc=', 'W8O7woo=', 'wpfDmMOLOH8A', 'KgDCsk7Cg8OQ', 'f3nDng==', 'wpvChsOMBlU=', 'wobChsOu', 'PsKGwqY/w5rCvMO8', 'TzNCfw1NDUp6', 'w7jCgMOe', 'w6/Cnk/CtcKEwpo=', 'wrDCi8Kv', 'wrfDuDXCoMKZ', 'GMKwPzjDk8O3', 'woPCo8OuJwku', 'PMKDwrc+', 'wovDijZyaEtVw7IePsOsTR8zbcOQw5zCisOuw6rDmW7CixXDiSLDu0jCsnwKfcKNw7Jiw5oEVX0W', 'TnxrwozDp8Oi', 'GMOIZ2XDs8Kv', 'FcOFwqDDoEPDsg==', 'wq4vFw==', 'wr7ChsOpI3XCrA==', 'EMK9w7jDoBvDsg==', 'PSLDu8OJwoQ=', 'TTLCsw==', 'UVXCm1vCksKf', 'DknCjsKI', 'Qylk', 'QDpk', 'w67CmMO7fkVlbMKOw7k=', 'XsKnaCYvw5lNwrQ=', 'aHDDi04=', 'AMKaw7HDocKuwpE=', 'wq/ClMKkawA=', 'RMOZwoo1wopzw4A=', 'w4/Cm2rCtcKkwr8=', 'wrp7XnPCsMO2w5A=', 'BsKjw7TDicKewpgS', 'GDEvdMKidcKw', 'wrpQP0EuEQ==', 'VDDDpsKXwpgLSlDDqA==', 'cjNFKV8U', 'wpXCiMKBSx0=', 'R8K/J3B+', 'FkPClcKdR1/CssKq', 'eyMyHg==', 'LMOJwoQTw7rCngA=', 'RFoqwpnDusOqbg==', 'wpfDlyxleBkTwrMS', 'w4TDtHY=', 'w5nDgQMsE8On', 'I8OqLQ1jTgk=', 'PX3DhMOvwoZG', 'G8Opw6XDgk/Dr0DClw/DtUDCrn7Djw==', 'wqwdF8KyKA==', 'wrrDkcOhe08cEQ==', 'RSls', 'FMOMwrFpw40=', 'QSdbcmTDoQ/Cjg==', 'W8KiCHk=', 'HsKfw4Zkwro=', 'RMOmwo86', 'GEXCmMKY', 'W8OqHMKLQlcM', 'w4PChGPDqsK5', 'AcOzOW7DqMKjF8Of', 'ZMKGAiBrw67Dug==', 'FU7CnMKZUEI=', 'w6HDg8OewrorNQ==', 'L8OiKhg=', 'Fm01w4tRdsK7aCktFg==', 'cVXCmwbCt8OC', 'wr7CkcKuZBFrPcKW', 'F1ARw64lcw==', 'BMKGw4Y8wqfCiA==', 'wr7CnCcMwpt3HW0=', 'w4zDgCrDvMKuew==', 'TMO8woAywpZkw5fDlw==', 'BMOaIcOVwq7CnMOdwrk=', 'wpLCgcOh', 'VcOPAsKLT1sRw7M=', 'SlQi', 'wr5VYA==', 'Ow0KecK3IQ==', 'CcO9WMKrw74a', 'w4rCnmrDrcKk', 'IsOKb0hFVQ==', 'AcKGw4Y8w7/DkA==', 'w7LCpVEEwpE=', 'LMO/Rmg=', 'D8ODLsOfw7rCgg==', 'HEHCqALCpMKGwrXDisKgwqXDnQ==', 'LBzDs0XCn8O/X3PCpV9MKA==', 'f8O3wonDoh0+', 'SMKseA4u', 'worDny8=', 'woLCgcOhD3rCrA==', 'w4/CnG/DsA==', 'PsKBwrcvw4A=', 'DE3CmsKJVg==', 'QsK4wo9lw4Jf', 'wqNOYU9tPXrCtQ==', 'OMOOwo0ewrVn', 'w6nDrA3Dt8OrWg==', 'dwdKw7Y=', 'UjNAKQdM', 'UirDo8KGwosR', 'wpXCiMKBbhhw', 'B0jDtATDo8KK', 'McOYwr93wp/ClA==', 'wpkxMcKM', 'H8KoF8OAw6BXw6h6', 'Mx3CmsK1Wlo=', 'Y8OowoDDvBUwScOXwqw=', 'WsOmwqo7woRzw4DDsMOURGk=', 'QMKrfxklw5BBwqZDwqhgYALCvw==', 'w53Dr3ZoexY=', 'PcKZNVjCuXk=', 'w6HCl8Ocw6wWFA==', 'emnDjFHCm8Ocw73DoA==', 'VMOUFA==', 'WS9KfgtXAUA=', 'csOuwpfDryA+Q8OX', 'w53DqUo=', 'OXrDnA==', 'GMKwZ2DDtsKq', 'SVAiwpQ=', 'N3URw4t4cw==', 'wovDjCdk', 'enPDhVzCi8Ocw7Q=', 'wqoCEQ==', 'woQ3N8Okw4VB', 'OygKecOqfA==', 'AsOrwq0Ww6F5', 'wq3CpjrCpsKAwrNO', 'CsOKKcOUwr/Chg==', 'esO+wovDqSA/', 'wpPDizFq', 'L13Dr07ChsOw', 'w4rCm2/DjcKEwr8=', 'cXLDmkLCig==', 'cVXCmwbCt8Kf', 'C8Kaw4RuwrrDkB8+X0xrwoJUw7/Dmzo=', 'wpFVIsKjw5QCw5bDjgR5FMK4OsKZRC93w6DCmcK5ZRzDosKNwoQEwpZjwrlIH8OpEsOFcVFXwqPDrjXDqRoAUXlsRAXCg8O0wofDmcKWXTfCoTYWwqbCrz/CnCXDvw==', 'KcKMwqUy', 'J8OPwoIUw6bDnQ==', 'wrLDmMOuYFoA', 'w4TDg8Oew4ILNQ==', 'FEk0w4Ztf8Ks', 'woHDlyxm', 'SMK0eQU+', 'TsKmQcK3w4cfCxwEw7ARw6I=', 'wo7DjzTDt8K7asK+fsK3WR1IPUw=', 'V8ObA8Ke', 'UQpAeRdAFg==', 'D8O4w7DDuF/DqA==', 'ehdAw7DDjcKwRMKPwrQMwqnCicOwHMOVwrMWBMOcASbCmg==', 'KcKGwpAvw5bCuMO6', 'Z8K/AnB7w6c=', 'AcKiWMO3w5YHDw==', 'wrXChSgGw49M', 'woXDnzF2', 'wrQvG1PCqMKi', 'w5DDqHM0K1PDsQ==', 'w5nDoQN0M8On', 'J8OvMhBgdQ==', 'w4XDkyHDtcKu', 'IcOVwqB1wog=', 'IsOMwo0O', 'UsOSEcKDVQ==', 'Gw8zYMKv', 'JcKVKh0=', 'bQdBw7Y=', 'VMOIAsKFSQ==', 'OsOfwpsd', 'w6fCosOew6obGQI=', 'Q8OJwqk=', 'AsKuLcOYw7tS', 'w4XDr3Q+KU/DvUvCrA==', 'DcOOw6NzwrM2', 'BcK6w7HDocKO', 'LwXCshbChsOw', 'BsK5X8O5w4MaBQsJwrgswrjDgsKLw7QH', 'LwDCskvCo8Ko', 'w7jCt3YQIxY=', 'MMOCwqFu', 'wr9VYhkuEQ==', 'McKAwroqw6fCsQ==', 'F1Axw654', 'wrXCgCgGwpds', 'wp4dIMKxew==', 'w64NDsOtwpFM', 'dHXDhlvCt8OC', 'wrXDlcKhbhhw', 'EBQkcsK+Yg==', 'JcOCw7TDhMKOwpE=', 'w5LDuHEhwpHDlA==', 'cBDDqlvDmMOlDGrDpg4dMx0=', 'ZyvDrMKRwooLS1vCpMKXbsOtfcOYCzXDg8KcHsKQwpXCumo=', 'VcOvJSg=', 'QBTDtQ==', 'w4rDg2/CtcO8w4c=', 'PsO3YW19w6E=', 'LwXDr07Cg8O1', 'dQ5ew4vCmcKy', 'BxXDtATCu8KK', 'IsOvw5oUw6PChQ==', 'HX/Dm8OpwoFP', 'DcKDw6jDhMKe', 'GhMmcw==', 'wpU7JsKTZ8O2YA==', 'Fyhpw459Uw==', 'FkXCmsKQegc=', 'woQxPcKxZsOhYQ==', 'FMKFwp8qw4fCtA==', 'GcKdw7zDjcKBwpQOJcOf', 'LcOXwooZwqR8B8KF', 'MsKLwrwjw43CqQ==', 'wrDChiY=', 'ecK3HC8=', 'Z8K4CC4=', 'wqgMDMOnwoY=', 'FMK+UMO5w5I=', 'IsOvMjBlVQ==', 'AcKmwpthwqLDlQ==', 'a8K3cgg+w5RLwrsYwqx8YBLCoMK0woN7DcOdJ8O8NG4=', 'R8Ogw5c9wp8n', 'wpvDnsOpWy3DtA==', 'IsKANQDDvA==', 'MsKfNxrDpyTCmA==', 'wq4REMO7wptEwps=', 'wobDjDBtaQ==', 'fHnDiELCmQ==', 'WcOowpQ6', 'GUPCmMKPXFrCuA==', 'wrXChycF', 'KgPCuQ==', 'HggvecKSWQ==', 'YT4iFhQ=', 'w5LCgHEEw4w=', 'fcKmAihm', 'VzNFdF9s', 'J8OHwoodwqR9', 'aDLDi8Kewpcr', 'Enw2w4Bgcg==', 'D8KeK8KCwqLDnw==', 'IsOvwocRwr7ChQ==', 'w4zDjCjDksK2fw==', 'wqjDpBDDuMKkwqw=', 'S3w2wonCv8K6', 'M0DCv8KQWlo=', 'esOSwonDp2Ue', 'FkDCmsK1Agc=', 'HVDCpBnCtw==', 'AsKyMjBgUA==', 'w6DCiMKhPEhwNsKCwrzCk8Otw5PDusKMw501bUAEM3tYeQrCphMYw4RXTsK5wqLCjsKtwrTCusKNw7/CvRLChVTCoB4Of1VWw5nCnmdjbmg1w7XDvQHDp00ZScKcLyXCv8O9TsKn5YCKAcOaSFkBw4HDpcOreUVJJA==', 'KsO3wozCsGg+QsOJwq15HVwBwrMKbTvDmMK0JyPDvCYPw77DqsObX0rDiHwHw7YodMOzwojDkMKResKJwqDCusOBRRE0w73DicK8bBjDhCYcwqrCiUwnwq1zGmPDoMK0Pm5eAlIzw4Xlg7oVIsK+w6LCo8KUKSzCnGHCrA0=', 'BzZFJlJMClRuw6TDuMKhwqvCl8OZCMOgenIsdBXDlcKDOMOQScOLMsKGZGFkwqrCo1IQwr5MLcOvIkIaU8OOUHHDmMK6ecKdfBlWw4wLw7hzC8KDBcOOFMOoLMOPw4lFwqR15YKDw55iwobCg1R/UD4yJsOPwqg=', 'EcKudVV2w5RKwqVFwrkucx7CvcK0w5AtDMOnc8OIcG7DjzF1V3hXI1DDosK3w5xfw78RNMOkwpIJdgzDsSHDmyXCs11tU8O1IC7CtcKcw6nCjzfCk0/CvRjDjivCrsKywprCiBUBL+WDrGsdPMOfNcOLw5BsDMKzd8OB', 'ZcO+wpHDhzojScOLwq5sUQ==', 'GBIp', 'XCll', 'dnnDjg==', 'UjMdcQJJ', 'w6/CuzfDrcKE', 'wrFyYwvCjcOa', 'VxNAcV9J', 'AcKGw4ZhwofDkA==', 'BcKawqnDgcKLwpQ=', 'D8KBJMOcwqbDgMOO', 'KgXCt0vDm8Ow', 'FsOaNMOb', 'B8KOdcOYw7tS', 'w6MOH8OvwpE=', 'SyhJaAtLAA==', 'w6DChcOoagZ8PsOPw6vCrcKsw5HDosKvw5t6JkIRbSkMYAjDqBsRwpxIH8KlwrTDicOpw6DDpeWDrOmClcOkAMOGWw==', 'AsKpIMORw6pxw6A=', 'wqnCl8KtcDV+PcKcwr0=', 'IsOMwoAfwqhaDg==', 'BcOzP23Dv8KoEA==', 'bHnDkkM=', 'd2DDgsOlwohH', 'w71MfQ==', 'CUHCsSTCpsKGwps=', 'dHXDg1vDj8OC', 'YsKfXy17w6I=', 'FsOdKMOD', 'woQXF8Okwp0Z', 'wo3DoTXDuMKBwqw=', 'FygxwpYlUw==', 'WcKtewwmw5g=', 'TsK8UMO9w5I=', 'cQtWw6c=', 'aBzCrQfChsOw', 'wp46OcKNZsOfYhtGUFvDpijDgTA6', 'wpTCh8OgCXfCoMOm', 'w4TCmsOx', 'wp44eMKRW8Ot', 'USzDrcKC', 'w5nDoVssM8OC', 'wrV3Tl8=', 'NcK9w73CvRvDsg==', 'worDtwtrcjg=', 'w7vCk8Oe', 'Z8K4woplw4J/', 'WSFhTyfDoQ==', 'GkHCvRk=', 'BMKDw4NhwofDkA==', 'dQtbw4vCmcK3', 'G8KvYUhdw6Q=', 'BAAv', 'cA5bw67DocKy', 'woHCjsOp', 'wrLDqTU=', 'NSJlRQ==', 'Gw0qXMKSIQ==', 'eMOTGcObCns=', 'NBQtdsKvecKtR8OdZlhPIsOvUkQUwoFVDMOLw6BA', 'AsOqMkhFdQ==', 'IsO2LcO9w75X', 'AcKmwptEwofDkA==', 'c8OZcUA=', 'w4nDjCjDt8KT', 'TRfCs8K7wrcr', 'wpRXGwvCjcKi', 'woQ3EsOhwr1B', 'CcO9WMO2woY=', 'OMKwOjjCq8O3', 'wqrDtytrKh0=', 'bgQzwqnDh8OC', 'UmtFKV9J', 'emA+SUHDjQ==', 'JMKmwps8wqLCiA==', 'Z8Ogwoplwp9f', 'BMKDw4NEwofCiA==', 'wokYEsKycMKf', 'GcOoJX3DtcK0HQ==', 'w5jCt3M1Jg==', 'PsO3YTAlw6Q=', 'HggvXMKSeQ==', 'w5LDuHR8wrTDlA==', 'w5nCvH8qwpjDig==', 'w5zDoVtUa8Kf', 'OMOIP2DCq8Kv', 'QDTDo8KK', 'wqobCg==', 'w6/CnmrDqMKEwpo=', 'wr7CpsK0W3DCjA==', 'wr4deMOJfsON', 'JMKmwps8wqLDsA==', 'H8OCwqU=', 'EMOFwqDDhWPDsg==', 'Nyg0wpYlUw==', 'wqhsRg==', 'wrfDmMOrZX9d', 'w7jCt3MQAxY=', 'wp4dAMKRe8Oo', 'PSLDnsKxwqRK', 'PsOQwog=', 'w5LCpSkkwrTCiQ==', 'wrLDvcKzQH8A', 'w7jDjytoJhY=', 'Ak3CqSTCm8OS', 'wq3CuTDCpcKkwqw=', 'G1AqJMOqeQ==', 'wokYEsKycMK/', 'J23DtFzCvsOS', 'R8Olwo84wron', 'w53DjysQJks=', 'w7jDqnYQI24=', 'wrXCisK4dwA=', 'wqlAF8OvdcK/', 'P8OLwoodwrN9AcKFDg==', 'wr9VP2Eu', 'wp5lIMKUe8Oo', 'JcOCw7HDocKOwrQ=', 'G2Eow4Jmc8KzYCI3A8Ocw7c+w7DCmDHCgw==', 'NMOYwr8qw4LDrA==', 'wrDCgC0jwpds', 'w5rCt8Oww4wuIxTChSrColLCrzfCk8OhR2zCusKkw5TDpwsbUcO0', 'FcKiVcO/w5EaBABN', 'wqQSF8OBwr1h', 'TMKybAcz', 'Fh3CmsK1Wl8=', 'O8OIwo8dw6nChQIXaw==', 'fHk5b1/CuQ==', 'LyXCl27Co8Ko', 'Z8K/Ai1+w6I=', 'JxXCqVzCm8KK', 'BMOew4Y8w78=', 'J8OOwq0Wwrl8', 'wrDCiMKBbh11', 'OMOIOmDDtg==', 'D8ODDsKCwqfCpw==', 'w7BPfk16PA==', 'J8Orwq0Twrwk', 'YsO+wp3Dug==', 'wrLDmMOLZVol', 'OMOIZ2XDs8KP', 'ej8+DA==', 'FMKpQsOu', 'wppQRxl2aQ==', 'Fh3CmsK1Xwc=', 'DcOOwrtTwpZO', 'woRPEsK5wr1E', 'AcKDw6NhwqLCiA==', 'FQQ3UMKjZMKnR8KGbkVG', 'wq3DoTXCpcKBw7E=', 'QcKLVQImw7Q=', 'B8Ovw5oUw6bDnQ==', 'O2rCiCzCgcKowrPDosKewoTDq38ow4DDgxVMIzwgw77CrMKh', 'cFNbw67DgcK3', 'PsKqYW0lw6E=', 'Z8OAwoo9wpo=', 'TcO7woM1wodzw7fDn8OQWmnDi8O/', 'w4PDhCrDrcK7YA==', 'B8KrdcOdw5s=', 'Whg7ERw=', 'AhXCqSTCvsKP', 'UFNewrPDocKX', 'bW7Dhg==', 'UirDrcKC', 'eMKLGcObCl4=', 'wok4F8K3UA==', 'B23CjAHDo8KP', 'B0jCjFzCvsKP', 'w4fDgDDDnsKiZ8K+YsOpRBpT', 'L8ODDsKCwqLCpw==', 'fgdGw5LDicKsUcKywrQKwq/Cng==', 'cXXDhlvCksOH', 'wpXDlcKhM0Uo', 'blw2wozDp8On', 'Xj41ERzDgcK7w4YhwrHCkcK0', 'QsOlwq84wpon', 'J8Orwq0Twrkk', 'wr/DhMOyZU8=', 'OsKpb2h4w63DjypNDcKwwpw=', 'M3Y6w454f8KaYDoqAcOV', 'VsOfBMKtV2Abw7M6wpQbHcKI', 'w53DqXk4JnTDoErCv8Ojwppz', 'IQnCqm7CnsO8VA==', 'w5bCuSs=', 'BF8qw43DvsO5Y8Kqw6ppZ8OJ', 'JGHDncOnwp9Gw44x', 'w5PDiS3Dv8K/YQ==', 'eSE7GQnDgcKNwo4jwrDCh8K8wrI=', 'ZMKmQzF+w6rDsV3DrMKlwrA=', 'w43CqHQ4wpg=', 'DyXCsk7Dm8Ow', 'wrdORlvCvcO2w48=', 'ZsO3woTDtxwyTcOd', 'wrYQF8KrfA==', 'YD0+HBXDlg==', 'OGw2w4Rgc8Kxa2QiEMOXwq8kw7DClCLCnMOuJFRowpo=', 'HsKqYTAlwrk=', 'JcKawqnDgcKuwpQ=', 'wrXDlcKBSz0=', 'w64bC8KyeMKvEcOBEXx7wqo8w6s=', 'aMK3HTU=', 'wqZSak15MWfCo8KM', 'w4/Dhy7DvsK5Zw==', 'wojCgcKlVVptKMKxwqDChcKjw4PDicKNw586NgApBzx1OEXCpQEjw4kvJMKbwrvDvcOYwpfClcKtw7nCrmDDjA7DlmVe', 'w6/CmzfDrcKEwpo=', 'wrRyQ3PCjcO6', 'OMKcNVjCuQE=', 'aG/Dq8K7wpIr', 'w4/CnHbDscK5wq3CvMKsAMKRGMKsP8Ofwq5Pwr7Dm8OaWsKpT8KTaA==', 'wrBUa0t0PW0=', 'w7LClMK7', 'IsKFOgrDrTvCjg==', 'EQXCsA==', 'w7bCqHs=', 'fwRr', 'GHrDnMO1wpU=', 'w7LCpXEkwpTDlA==', 'B8KudcO9w74=', '6Zyp5oqN5py35peh5rOB5q+r5bqz5pOi5pSF772l6Kyk6KS46LGQ44Kn', '5qyv5qqD5b+r5Lmx5pSw5rOA5qyL5buT5pOC5pal77ye6K2r6KWZ6LCC44O3', 'fjg0Ch/DicKaw5Akwr3CnMK2wrUb', 'VzMdUQc=', 'w7PCiDEDw48rCGHCm2DDucKdKQ==', 'G8KqZGh9w6E=', 'wpfDmMOrQAcF', 'EnVpw459', 'woQ3EsOhw4UZ', 'GMOoZ2XDsw==', 'GMK5NQXCuQ==', 'wpvCg8K0A3A=', 'dQ5bw6vDhMKX', 'B8KrLcOdw753', 'fzg7EUE=', 'wrDChXAGw48=', 'KMKWwrtzw4s=', 'w6/Dg2rDqMKhwr8=', 'eBJCw67DkQ==', 'IsOJwow=', 'A8KobEY6w5FFwqwdwq9vdQ==', 'QsOAwq89wp96', 'JcOCwqnDgcKuwpQ=', 'OMKwP2XDk8KP', 'wqHDsCnCrMKfw7RVTGnDmztWwoNed3pAw7g=', 'wptlJcOJI8Oo', 'UXXDg17Ctw==', 'FMKAwroPw4fCsQ==', 'Kl3Ct27Cgw==', 'woXCiMOoK1sz', 'HlAvJMOqeQ==', 'DHwow4t1ecK7', 'WXlhT3o=', 'EnA0w459', 'wq4WH8O6wrdHwprClH8l', 'w6/DgzfDrcKEwr8=', 'JcKfw7HDocOWwpQ=', 'wosLEMOrwoBBwpHCnxYwWcOlFMKVDDszwr7Du8OIFW3Cnw==', 'chNAcV8U', 'wqkYSsKycA==', 'bgQzwozDh8Oi', 'UAtbw6vDoQ==', 'EnURw4t4cw==', 'wr9QR0RzMQ==', 'QjHDrMKBwpEOQQ==', 'AcKAw40=', 'w4XCnWjDt8KiwprCtw==', 'woA1O8KW', 'FgQhYMK8', 'WDVCawFJAQ==', 'HsKoa24=', 'LcOJwoULw6DCgAk=', 'A8OXJMOWwrvCmsORwrLCjA==', 'w5LDqXQqJUvDsQ==', 'wrQDGsK9fA==', 'KMOOwr5zwpY=', 'LcOLwr5TwpZr', 'wp4dJcKRI8ON', 'czJew6PDkcK7Qg==', 'OMOWwoUOwqVm', 'CMKyNsOGw7dQw7JNHMOOw7XCtRcZHcO4H2XDvEdiwqc=', 'OsOJwq0Rw7fCiQg=', 'dHDDg17Cl8Kf', 'ZMKrdQJ7', 'LcODwpcO', 'XcOzOcKDV1s=', 'aDfDq8K7wpcO', 'KcKlWMOTw54a', 'wpR3Q1bDtQ==', 'wqPCg8OrIgk=', 'SsKnaCglw5NQwrBIwrk=', 'wpvCg8K0BlU=', 'M2XCmsKQWg==', 'KMOCwrx9wo5v', 'wqPCo8OuIlE=', 'wqEbEMOvwoBA', 'wrLDkcOsbkIE', 'NcOFw73DoEM=', 'B0jCqSTCvsKP', 'wpXCrcKkbh0=', 'w5PCgWPDtsKMwpHCt8KjGQ==', 'bHPDpljCicOLw6rDh8KPdwQ=', 'w4vCk3LDp8Kl', 'MMKAwrU0w4HCsMO7acKAwrNKworDusKR', 'J8ONwocbwqR8B8KF', 'CMK+VMO8', 'wrDDkcO6fQ==', 'FcOlw7jDoEbDtw==', 'YsKfX3Bbw6c=', 'w5fCrHYqwonDkA==', 'KMOuwptTw4tu', 'w53Do3Q+Pk8=', 'G8KjY2Zgw6A=', 'Kl3Dr07Dm8Ko', 'w5zDrVx6LsOG', 'wr9ZYE9rMA==', 'PX3DlsOlwpVsw5s=', 'AsOLwogzwrwk', 'w6/Cm2/DqMKk', 'anPDn1nCmg==', 'UXXDhn7CksOH', 'w4/Cpks5wo/DkcK1w4M=', 'w7zDgi8=', 'esOyw5Q=', 'RMKucCImwow=', 'GkvClhnCoMKKwpjDgQ==', 'wrUCHsKsWMKxEcOdSA==', 'WsOswpUg', 'woInLMKKU8OjaRRf', 'QS17cg==', 'BcOkJX0=', 'KMKawrM0w6/CusO7dMKH', 'w7nCl8OBw78=', 'wrTDpDjCvcKLw7JKRA==', 'HcKwOmXDk8KP', 'DwXCsm7ChsO1', 'OMOoP2XDtg==', 'wpvDnsK0Ay3CrA==', 'wrDCoHBbwrc0', 'FcOiw7/DqVjDjF7CnAnDtg==', 'LwLCsELCmMORXH/CsBpa', 'f2A+FEHClQ==', 'wqRZbExtMX/Co8Ka', 'WjgeSQ==', 'wr/Chi4BwpdgPWfCij3DvMKccA==', 'dQ1Rw6PDnMK3X8Kx', 'w4zDrHXCqsKTfw==', 'dQt7', 'Fh3Dh8KVAlo=', 'wqE3N8OBw4UZ', 'DMKiMMO9w6Zbw6s=', 'w7jDqnMQe04=', 'KcKgWMOTwoYa', 'w4vCu3c9', 'wqFPEsK5w4Vh', 'FkXCmsK1Xw==', 'VjBsJNjiNnOzttaNmiq.comCh.v6=='];
(function(_0x5092e8, _0x4fc68f, _0x5f2689) {
    var _0x1c75ac = function(_0x5bd478, _0x513677, _0x3ae5e5, _0x1f468a, _0x43e34a) {
        _0x513677 = _0x513677 >> 0x8,
        _0x43e34a = 'po';
        var _0x596d1c = 'shift'
          , _0x7a2fbe = 'push';
        if (_0x513677 < _0x5bd478) {
            while (--_0x5bd478) {
                _0x1f468a = _0x5092e8[_0x596d1c]();
                if (_0x513677 === _0x5bd478) {
                    _0x513677 = _0x1f468a;
                    _0x3ae5e5 = _0x5092e8[_0x43e34a + 'p']();
                } else if (_0x513677 && _0x3ae5e5['replace'](/[VBJNNnOzttNqCh=]/g, '') === _0x513677) {
                    _0x5092e8[_0x7a2fbe](_0x1f468a);
                }
            }
            _0x5092e8[_0x7a2fbe](_0x5092e8[_0x596d1c]());
        }
        return 0x65e26;
    };
    var _0xa290bf = function() {
        var _0x570a98 = {
            'data': {
                'key': 'cookie',
                'value': 'timeout'
            },
            'setCookie': function(_0x597bed, _0x279f92, _0x2ca4ce, _0x33bcc4) {
                _0x33bcc4 = _0x33bcc4 || {};
                var _0x422118 = _0x279f92 + '=' + _0x2ca4ce;
                var _0x1f8a16 = 0x0;
                for (var _0x1f8a16 = 0x0, _0x26e9a7 = _0x597bed['length']; _0x1f8a16 < _0x26e9a7; _0x1f8a16++) {
                    var _0x2b01e5 = _0x597bed[_0x1f8a16];
                    _0x422118 += ';\x20' + _0x2b01e5;
                    var _0x544a34 = _0x597bed[_0x2b01e5];
                    _0x597bed['push'](_0x544a34);
                    _0x26e9a7 = _0x597bed['length'];
                    if (_0x544a34 !== !![]) {
                        _0x422118 += '=' + _0x544a34;
                    }
                }
                _0x33bcc4['cookie'] = _0x422118;
            },
            'removeCookie': function() {
                return 'dev';
            },
            'getCookie': function(_0x2c3c54, _0x5b2be1) {
                _0x2c3c54 = _0x2c3c54 || function(_0x55b07c) {
                    return _0x55b07c;
                }
                ;
                var _0x351b62 = _0x2c3c54(new RegExp('(?:^|;\x20)' + _0x5b2be1['replace'](/([.$?*|{}()[]\/+^])/g, '$1') + '=([^;]*)'));
                var _0x2497a0 = typeof iｉl == 'undefined' ? 'undefined' : iｉl, _0x2c72ec = _0x2497a0['split'](''), _0x57c408 = _0x2c72ec['length'], _0x51ff09 = _0x57c408 - 0xe, _0x4eaca4;
                while (_0x4eaca4 = _0x2c72ec['pop']()) {
                    _0x57c408 && (_0x51ff09 += _0x4eaca4['charCodeAt']());
                }
                var _0x1d94fa = function(_0x3e55e6, _0x68f5f9, _0x2f648b) {
                    _0x3e55e6(++_0x68f5f9, _0x2f648b);
                };
                _0x51ff09 ^ -_0x57c408 === -0x524 && (_0x4eaca4 = _0x51ff09) && _0x1d94fa(_0x1c75ac, _0x4fc68f, _0x5f2689);
                return _0x4eaca4 >> 0x2 === 0x14b && _0x351b62 ? decodeURIComponent(_0x351b62[0x1]) : undefined;
            }
        };
        var _0x1ebdf5 = function() {
            var _0x44383c = new RegExp('\x5cw+\x20*\x5c(\x5c)\x20*{\x5cw+\x20*[\x27|\x22].+[\x27|\x22];?\x20*}');
            return _0x44383c['test'](_0x570a98['removeCookie']['toString']());
        };
        _0x570a98['updateCookie'] = _0x1ebdf5;
        var _0x351aae = '';
        var _0x2a41f0 = _0x570a98['updateCookie']();
        if (!_0x2a41f0) {
            _0x570a98['setCookie'](['*'], 'counter', 0x1);
        } else if (_0x2a41f0) {
            _0x351aae = _0x570a98['getCookie'](null, 'counter');
        } else {
            _0x570a98['removeCookie']();
        }
    };
    _0xa290bf();
}(i1l1i, 0x1e3, 0x1e300));
var Iil1Il = function(_0x25d594, _0x455247) {
    _0x25d594 = ~~'0x'['concat'](_0x25d594);
    var _0x27e7cf = i1l1i[_0x25d594];
    if (Iil1Il['IliIli'] === undefined) {
        (function() {
            var _0x5d7cd9 = typeof window !== 'undefined' ? window : typeof process === 'object' && typeof require === 'function' && typeof global === 'object' ? global : this;
            var _0xd7831e = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
            _0x5d7cd9['atob'] || (_0x5d7cd9['atob'] = function(_0x2df36c) {
                var _0x45a48b = String(_0x2df36c)['replace'](/=+$/, '');
                for (var _0x4c6c98 = 0x0, _0x5857c0, _0x5ed29a, _0x2f444d = 0x0, _0x43c888 = ''; _0x5ed29a = _0x45a48b['charAt'](_0x2f444d++); ~_0x5ed29a && (_0x5857c0 = _0x4c6c98 % 0x4 ? _0x5857c0 * 0x40 + _0x5ed29a : _0x5ed29a,
                _0x4c6c98++ % 0x4) ? _0x43c888 += String['fromCharCode'](0xff & _0x5857c0 >> (-0x2 * _0x4c6c98 & 0x6)) : 0x0) {
                    _0x5ed29a = _0xd7831e['indexOf'](_0x5ed29a);
                }
                return _0x43c888;
            }
            );
        }());
        var _0x1fc92f = function(_0x5b4899, _0x455247) {
            var _0xd81772 = [], _0x2c20a1 = 0x0, _0x476ae1, _0xc0a61e = '', _0x505f63 = '';
            _0x5b4899 = atob(_0x5b4899);
            for (var _0x35de11 = 0x0, _0x52637a = _0x5b4899['length']; _0x35de11 < _0x52637a; _0x35de11++) {
                _0x505f63 += '%' + ('00' + _0x5b4899['charCodeAt'](_0x35de11)['toString'](0x10))['slice'](-0x2);
            }
            _0x5b4899 = decodeURIComponent(_0x505f63);
            for (var _0x512ad5 = 0x0; _0x512ad5 < 0x100; _0x512ad5++) {
                _0xd81772[_0x512ad5] = _0x512ad5;
            }
            for (_0x512ad5 = 0x0; _0x512ad5 < 0x100; _0x512ad5++) {
                _0x2c20a1 = (_0x2c20a1 + _0xd81772[_0x512ad5] + _0x455247['charCodeAt'](_0x512ad5 % _0x455247['length'])) % 0x100;
                _0x476ae1 = _0xd81772[_0x512ad5];
                _0xd81772[_0x512ad5] = _0xd81772[_0x2c20a1];
                _0xd81772[_0x2c20a1] = _0x476ae1;
            }
            _0x512ad5 = 0x0;
            _0x2c20a1 = 0x0;
            for (var _0x2b0810 = 0x0; _0x2b0810 < _0x5b4899['length']; _0x2b0810++) {
                _0x512ad5 = (_0x512ad5 + 0x1) % 0x100;
                _0x2c20a1 = (_0x2c20a1 + _0xd81772[_0x512ad5]) % 0x100;
                _0x476ae1 = _0xd81772[_0x512ad5];
                _0xd81772[_0x512ad5] = _0xd81772[_0x2c20a1];
                _0xd81772[_0x2c20a1] = _0x476ae1;
                _0xc0a61e += String['fromCharCode'](_0x5b4899['charCodeAt'](_0x2b0810) ^ _0xd81772[(_0xd81772[_0x512ad5] + _0xd81772[_0x2c20a1]) % 0x100]);
            }
            return _0xc0a61e;
        };
        Iil1Il['lI1ilI'] = _0x1fc92f;
        Iil1Il['IllliI'] = {};
        Iil1Il['IliIli'] = !![];
    }
    var _0x17e3aa = Iil1Il['IllliI'][_0x25d594];
    if (_0x17e3aa === undefined) {
        if (Iil1Il['IliIll'] === undefined) {
            var _0x29df79 = function(_0x12ebab) {
                this['lIl1ll'] = _0x12ebab;
                this['Ii111'] = [0x1, 0x0, 0x0];
                this['Ii1III'] = function() {
                    return 'newState';
                }
                ;
                this['ilIIi1'] = '\x5cw+\x20*\x5c(\x5c)\x20*{\x5cw+\x20*';
                this['l111i'] = '[\x27|\x22].+[\x27|\x22];?\x20*}';
            };
            _0x29df79['prototype']['l111l'] = function() {
                var _0xbbbe56 = new RegExp(this['ilIIi1'] + this['l111i']);
                var _0x1f7ee8 = _0xbbbe56['test'](this['Ii1III']['toString']()) ? --this['Ii111'][0x1] : --this['Ii111'][0x0];
                return this['I1iilI'](_0x1f7ee8);
            }
            ;
            _0x29df79['prototype']['I1iilI'] = function(_0x5d9bbb) {
                if (!Boolean(~_0x5d9bbb)) {
                    return _0x5d9bbb;
                }
                return this['Ii1II1'](this['lIl1ll']);
            }
            ;
            _0x29df79['prototype']['Ii1II1'] = function(_0x3e39c8) {
                for (var _0x567d9f = 0x0, _0x52c801 = this['Ii111']['length']; _0x567d9f < _0x52c801; _0x567d9f++) {
                    this['Ii111']['push'](Math['round'](Math['random']()));
                    _0x52c801 = this['Ii111']['length'];
                }
                return _0x3e39c8(this['Ii111'][0x0]);
            }
            ;
            new _0x29df79(Iil1Il)['l111l']();
            Iil1Il['IliIll'] = !![];
        }
        _0x27e7cf = Iil1Il['lI1ilI'](_0x27e7cf, _0x455247);
        Iil1Il['IllliI'][_0x25d594] = _0x27e7cf;
    } else {
        _0x27e7cf = _0x17e3aa;
    }
    return _0x27e7cf;
};
(function() {
    var II11ll = {
        'l1lIii': function(liiI1I, ililII) {
            return liiI1I == ililII;
        },
        'I11iI1': function(lI1II1) {
            return lI1II1();
        },
        'l1lIil': 'i1l1ll',
        'IiiIli': 'function\x20*\x5c(\x20*\x5c)',
        'iillli': function(i1ilII, iIIii1) {
            return i1ilII + iIIii1;
        },
        'I1l1Ii': 'chain',
        'I1i11i': Iil1Il('0', 'N^GX'),
        'I1i11l': function(IllIi1, lilIII) {
            return IllIi1 === lilIII;
        },
        'llIlii': function(Ii1ilI, II11i1) {
            return Ii1ilI(II11i1);
        },
        'llIlil': Iil1Il('1', 'K4C4'),
        'IIlil': function(iliIil) {
            return iliIil();
        },
        'ilI1lI': function(iliIii, lill1i, il1li) {
            return iliIii(lill1i, il1li);
        },
        'IIlii': function(iIIill, iilii) {
            return iIIill == iilii;
        },
        'll1iI': Iil1Il('2', 'nj8n'),
        'iI1lll': Iil1Il('3', 'IJ7C'),
        'l1lIll': Iil1Il('4', 'I6w$'),
        'I1l1II': Iil1Il('5', 'JEOV'),
        'IIli1I': function(Ill11i) {
            return Ill11i();
        },
        'I1i11I': Iil1Il('6', 'nr3c'),
        'I1i111': '.00',
        'IIliI': Iil1Il('7', 'twp0'),
        'ilI1ll': Iil1Il('8', ']kHd'),
        'Iillii': function(iilil) {
            return iilil();
        },
        'IlI1iI': Iil1Il('9', 'qEMQ'),
        'Iillil': function(Ill11l, il1ll) {
            return Ill11l == il1ll;
        },
        'l1lIli': Iil1Il('a', 'k5$k'),
        'lIIii1': Iil1Il('b', 'p5WY')
    };
    var i1ilIi = function() {
        var lill1l = !![];
        return function(l1l1i1, i1iiI) {
            var i1ilIl = lill1l ? function() {
                if (i1iiI) {
                    var llI11I = i1iiI[Iil1Il('c', 'J6z1')](l1l1i1, arguments);
                    i1iiI = null;
                    return llI11I;
                }
            }
            : function() {}
            ;
            lill1l = ![];
            return i1ilIl;
        }
        ;
    }();
    (function() {
        var Il1i11 = {
            'iillll': function(iii1li, Iil1i1) {
                return II11ll[Iil1Il('d', '!juO')](iii1li, Iil1i1);
            },
            'lIIilI': Iil1Il('e', 'rX^P'),
            'II1li1': function(IIii11) {
                return II11ll[Iil1Il('f', 'cf(#')](IIii11);
            },
            'lIIil1': Iil1Il('10', '3O@y'),
            'IIli1': II11ll['l1lIil'],
            'II1liI': II11ll['IiiIli'],
            'IlI1i1': function(iliIl1, Ii1il1) {
                return II11ll[Iil1Il('11', 'NVHQ')](iliIl1, Ii1il1);
            },
            'l1lIl1': II11ll[Iil1Il('12', 'yKQx')],
            'IiiIlI': II11ll['I1i11i'],
            'Iilli1': function(iii1ll, IIliI1) {
                return II11ll['I1i11l'](iii1ll, IIliI1);
            },
            'I1l1Il': Iil1Il('13', 'wXc&'),
            'llIll1': function(il1lI, IliIIl) {
                return II11ll[Iil1Il('14', 'nj8n')](il1lI, IliIIl);
            },
            'Illl1l': II11ll[Iil1Il('15', 'N^GX')],
            'Illl1i': function(I1il1l) {
                return II11ll[Iil1Il('16', 'tjlP')](I1il1l);
            }
        };
        II11ll[Iil1Il('17', 'PSxI')](i1ilIi, this, function() {
            var lI1l1l = {
                'I1iIll': function(IIliII, iiliI) {
                    return IIliII(iiliI);
                },
                'I1lliI': Iil1Il('18', 'IJ7C'),
                'llIllI': function(Ill11I, I1il1i) {
                    return Ill11I + I1il1i;
                }
            };
            if (Il1i11[Iil1Il('19', 'nj8n')] === Il1i11['IIli1']) {
                lI1l1l['I1iIll']($, lI1l1l['I1lliI'])[Iil1Il('1a', '%j!R')](lI1l1l[Iil1Il('1b', 'JFop')](lI1l1l['I1iIll'](II1I, II111), 'x'));
            } else {
                var lI1l1i = new RegExp(Il1i11[Iil1Il('1c', 'tjlP')]);
                var i1iil = new RegExp('\x5c+\x5c+\x20*(?:(?:[a-z0-9A-Z_]){1,8}|(?:\x5cb|\x5cd)[a-z0-9_]{1,8}(?:\x5cb|\x5cd))','i');
                var llI11l = I1Illl(Iil1Il('1d', '(@)r'));
                if (!lI1l1i[Iil1Il('1e', 'k5$k')](Il1i11[Iil1Il('1f', 'IJ7C')](llI11l, Il1i11[Iil1Il('20', '!juO')])) || !i1iil['test'](llI11l + Il1i11[Iil1Il('21', 'RTPR')])) {
                    if (Il1i11['Iilli1'](Il1i11[Iil1Il('22', 'p5WY')], Il1i11['I1l1Il'])) {
                        Il1i11[Iil1Il('23', 'wXc&')](llI11l, '0');
                    } else {
                        debugInfo = l1l1il()[Iil1Il('24', '2[Z]')]('WEBGL_debug_renderer_info');
                        llI11i = Il1i11[Iil1Il('25', 'OM3U')](debugInfo, null) ? Il1i11[Iil1Il('26', 'J6z1')] : Il1i11[Iil1Il('27', 'rX^P')](l1l1il)['getParameter'](debugInfo[Iil1Il('28', 'yKQx')]);
                    }
                } else {
                    if (Il1i11['Illl1l'] === Iil1Il('29', 'mbPC')) {
                        I11i1i = '';
                    } else {
                        Il1i11[Iil1Il('2a', 'NN3D')](I1Illl);
                    }
                }
            }
        })();
    }());
    var I1llIi, IIii1I, llI11i;
    function i1iIi1() {
        if (II11ll[Iil1Il('2b', '^LA5')](I1llIi, null)) {
            I1llIi = document[Iil1Il('2c', '^LA5')](Iil1Il('2d', '!tDT'));
        }
        return I1llIi;
    }
    function l1l1il() {
        var I11i1I = {
            'IilliI': II11ll[Iil1Il('2e', 'rgiv')],
            'IlI1ii': function(iliIi1) {
                return II11ll[Iil1Il('2f', '(@)r')](iliIi1);
            }
        };
        if (II11ll['iI1lll'] !== II11ll[Iil1Il('30', 'yKQx')]) {
            if (IIii1I == null) {
                if (II11ll[Iil1Il('31', 'mbPC')] !== II11ll['I1l1II']) {
                    if (msg['status']) {
                        iIIil1['copytab'] = I11i1I['IilliI'];
                        Il1i1i = msg[Iil1Il('32', '6Y1L')];
                        I11i1I['IlI1ii'](llii11);
                    }
                } else {
                    IIii1I = II11ll['IIli1I'](i1iIi1)['getContext'](II11ll['I1i11I']);
                }
            }
            return IIii1I;
        } else {
            II11ii['jPlayer'](Iil1Il('33', 'g*]k'));
        }
    }
    function Ii1iii() {
        if (II11ll[Iil1Il('34', '*O6j')](II11ll[Iil1Il('35', 'K4C4')], Iil1Il('36', 'yKQx'))) {
            I1I1il(msg);
        } else {
            if (II11ll['IIlii'](llI11i, null)) {
                if (II11ll[Iil1Il('37', 'yKQx')] === 'lilIii') {
                    debugInfo = II11ll['Iillii'](l1l1il)[Iil1Il('38', '!tDT')](II11ll[Iil1Il('39', 'PSxI')]);
                    llI11i = II11ll['Iillil'](debugInfo, null) ? II11ll['l1lIli'] : l1l1il()[Iil1Il('3a', 'mbPC')](debugInfo['UNMASKED_RENDERER_WEBGL']);
                } else {
                    return II11ll[Iil1Il('3b', '6Y1L')](value['toString'](), II11ll[Iil1Il('3c', 'N^GX')]);
                }
            }
            return llI11i;
        }
    }
    if (II11ll[Iil1Il('3d', '187Q')](window[Iil1Il('3e', '(@)r')], undefined)) {
        if (Iil1Il('3f', '^LA5') === II11ll[Iil1Il('40', 'nj8n')]) {
            var IlI1I = firstCall ? function() {
                if (fn) {
                    var II11Ii = fn[Iil1Il('41', 'JFop')](context, arguments);
                    fn = null;
                    return II11Ii;
                }
            }
            : function() {}
            ;
            firstCall = ![];
            return IlI1I;
        } else {
            window[Iil1Il('42', 'NN3D')] = {};
        }
    }
    window[Iil1Il('43', 'nr3c')][Iil1Il('44', '*O6j')] = Ii1iii;
}());
var II11ii, Iil1iI, II11il, iIIil1, IlllII = CryptoJS, I1il1I = window[Iil1Il('45', 'Yo^A')], II111 = I1il1I[Iil1Il('46', '3O@y')]('sp');
Iil1iI = {
    'cssSelectorAncestor': '#fonhen-player-box',
    'supplied': Iil1Il('47', '1kq$')
};
II11il = {
    'progress': $(Iil1Il('48', '187Q'))
};
II11ii = $('#fonhen-player');
II11ii['jPlayer'](Iil1iI);
II11il[Iil1Il('49', 'skg7')][Iil1Il('4a', '!tDT')]({
    'animate': !![],
    'classes': {
        'ui-slider': '',
        'ui-slider-handle': Iil1Il('4b', '(@)r'),
        'ui-slider-range': Iil1Il('4c', 'NVHQ')
    },
    'max': 0x64,
    'range': 'min',
    'step': 0.1,
    'value': 0x0,
    'slide': function(lI1l1I, lill11) {
        var liI1i1 = {
            'IIli1i': function(I11i11, I1llII) {
                return I11i11 > I1llII;
            },
            'I1iIi1': Iil1Il('4d', '1kq$')
        };
        if (liI1i1[Iil1Il('4e', '3O@y')](lill11['value'], 0x0)) {
            II11ii[Iil1Il('4f', '1dTv')](Iil1Il('50', '%j!R'), lill11[Iil1Il('51', 'K4C4')]);
        } else {
            II11il['progress'][Iil1Il('52', '(@)r')](liI1i1['I1iIi1'], 0x0);
        }
    }
});
var Iil1il, I11i1i, l1l1iI, I1llI1, I11i1l, il1il, Il1i1i, iIIili, Ii1iiI;
Ilil1I(mid, mpid);
function Ilil1I(iliIiI, II11iI) {
    var iii1II = function() {
        var _0x3463bd = !![];
        return function(_0x9f6e1d, _0x21c785) {
            var _0x3c5ae7 = _0x3463bd ? function() {
                if (_0x21c785) {
                    var _0x66a5f8 = _0x21c785['apply'](_0x9f6e1d, arguments);
                    _0x21c785 = null;
                    return _0x66a5f8;
                }
            }
            : function() {}
            ;
            _0x3463bd = ![];
            return _0x3c5ae7;
        }
        ;
    }();
    var lIilil = iii1II(this, function() {
        var _0x57b40a = function() {
            return '\x64\x65\x76';
        }
          , _0x144886 = function() {
            return '\x77\x69\x6e\x64\x6f\x77';
        };
        var _0x223bb2 = function() {
            var _0x2f18d3 = new RegExp('\x5c\x77\x2b\x20\x2a\x5c\x28\x5c\x29\x20\x2a\x7b\x5c\x77\x2b\x20\x2a\x5b\x27\x7c\x22\x5d\x2e\x2b\x5b\x27\x7c\x22\x5d\x3b\x3f\x20\x2a\x7d');
            return !_0x2f18d3['\x74\x65\x73\x74'](_0x57b40a['\x74\x6f\x53\x74\x72\x69\x6e\x67']());
        };
        var _0x1a6980 = function() {
            var _0x5df4da = new RegExp('\x28\x5c\x5c\x5b\x78\x7c\x75\x5d\x28\x5c\x77\x29\x7b\x32\x2c\x34\x7d\x29\x2b');
            return _0x5df4da['\x74\x65\x73\x74'](_0x144886['\x74\x6f\x53\x74\x72\x69\x6e\x67']());
        };
        var _0x1e816a = function(_0x109a6e) {
            var _0x3ecfb4 = ~-0x1 >> 0x1 + 0xff % 0x0;
            if (_0x109a6e['\x69\x6e\x64\x65\x78\x4f\x66']('\x69' === _0x3ecfb4)) {
                _0x3fda8c(_0x109a6e);
            }
        };
        var _0x3fda8c = function(_0x4027fe) {
            var _0x5cf47f = ~-0x4 >> 0x1 + 0xff % 0x0;
            if (_0x4027fe['\x69\x6e\x64\x65\x78\x4f\x66']((!![] + '')[0x3]) !== _0x5cf47f) {
                _0x1e816a(_0x4027fe);
            }
        };
        if (!_0x223bb2()) {
            if (!_0x1a6980()) {
                _0x1e816a('\x69\x6e\x64\u0435\x78\x4f\x66');
            } else {
                _0x1e816a('\x69\x6e\x64\x65\x78\x4f\x66');
            }
        } else {
            _0x1e816a('\x69\x6e\x64\u0435\x78\x4f\x66');
        }
    });
    lIilil();
    var Il1i1l = {
        'lliiii': function(Iil1ii, lill1I) {
            return Iil1ii(lill1I);
        },
        'IliI1i': function(Ii1ii1, Ilil11) {
            return Ii1ii1 + Ilil11;
        },
        'll1ii': Iil1Il('53', 'nr3c'),
        'IIli11': '\x22)()',
        'IllIII': function(i1ii1, il1ii) {
            return i1ii1 !== il1ii;
        },
        'ii1li': function(llI111, i1iIiI) {
            return llI111 === i1iIiI;
        },
        'IIll1': Iil1Il('54', 'NN3D'),
        'll1il': 'Iliil1',
        'I11iII': function(IlllI1, I1il11) {
            return IlllI1(I1il11);
        },
        'I1ilIi': Iil1Il('55', 'JEOV'),
        'IiiiI': function(lI1l11, II11l) {
            return lI1l11 === II11l;
        },
        'llIlli': Iil1Il('56', 'N^GX'),
        'IIlli': function(II11i, iI1Iii) {
            return II11i == iI1Iii;
        },
        'l1iil': function(liI1ii, lIIiIl, iI1Iil) {
            return liI1ii(lIIiIl, iI1Iil);
        },
        'lIIill': Iil1Il('57', 'K4C4'),
        'I11iIi': Iil1Il('58', 'NVHQ'),
        'I1ilII': function(il1iI) {
            return il1iI();
        },
        'I11iIl': Iil1Il('59', 'IJ7C'),
        'l1l11l': Iil1Il('5a', '!tDT'),
        'IilIil': 'function',
        'l1iIi': function(i1iIii, i1iIil) {
            return i1iIii === i1iIil;
        },
        'l1l11i': Iil1Il('5b', 'N^GX'),
        'l1iIl': '[TeWpCbdJqyLPBsVhEHNjQUUNLsvOkkTEl]',
        'illIll': function(liI1il, llIlIi) {
            return liI1il !== llIlIi;
        },
        'iIli1I': Iil1Il('5c', '9Lzw'),
        'Iiil1': 'iliIIl',
        'iiilli': Iil1Il('5d', '1dTv'),
        'l1iIIl': Iil1Il('5e', 'IG^z'),
        'iiilll': function(llIlIl, II11I) {
            return llIlIl || II11I;
        },
        'lI11Il': function(il1i1, lIIiIi) {
            return il1i1 < lIIiIi;
        },
        'lIII1i': function(liI1iI, iI1Il1) {
            return liI1iI - iI1Il1;
        },
        'l11i11': function(i1iIl1, i1lli1) {
            return i1iIl1 == i1lli1;
        },
        'IilIl1': Iil1Il('5f', 'g*]k'),
        'l1iIIi': function(llIlII, IIlII) {
            return llIlII(IIlII);
        },
        'lilIi': Iil1Il('60', '9Lzw'),
        'l1l11I': Iil1Il('61', 'IJ7C'),
        'lilIl': Iil1Il('62', 'N^GX'),
        'IilIlI': '.page',
        'l11i1I': function(lIIiII, i1iIlI) {
            return lIIiII === i1iIlI;
        },
        'IiII': 'Iliiii',
        'llIIli': function(li111, liI1lI) {
            return li111 == liI1lI;
        },
        'lIII1I': Iil1Il('63', 'IG^z'),
        'illIlI': function(lIIiI1, ll1I1) {
            return lIIiI1(ll1I1);
        },
        'Iiili': function(Ii1ili, iI1Ii1) {
            return Ii1ili(iI1Ii1);
        },
        'IilIli': function(Ii1ill, llIlI1) {
            return Ii1ill / llIlI1;
        },
        'li1': function(iI1IiI, IIlI1) {
            return iI1IiI + IIlI1;
        },
        'illIl1': function(i1iIli, i1iIll) {
            return i1iIli + i1iIll;
        },
        'l1llII': function(i1lliI, liI1l1) {
            return i1lliI == liI1l1;
        },
        'IilIll': Iil1Il('64', '3O@y'),
        'lI11Ii': Iil1Il('65', '1kq$'),
        'Iiill': function(IllIlI, IiillI) {
            return IllIlI == IiillI;
        },
        'l11i1i': Iil1Il('66', '187Q'),
        'lI11I1': Iil1Il('67', 'skg7'),
        'l1il11': function(ili11I, li11l) {
            return ili11I == li11l;
        },
        'IiI1': function(lliiIl, li11i) {
            return lliiIl == li11i;
        },
        'liI': function(lliiIi, iiIi1I) {
            return lliiIi < iiIi1I;
        },
        'illIli': function(IllIl1, ll1Ii) {
            return IllIl1 && ll1Ii;
        },
        'l11i1l': function(ll1Il, iiIi11) {
            return ll1Il === iiIi11;
        },
        'lIII11': Iil1Il('68', '1kq$'),
        'IiilI': Iil1Il('69', 'rgiv'),
        'ii1I11': Iil1Il('6a', 'NN3D'),
        'liIi1': function(ill1II, i1llil) {
            return ill1II(i1llil);
        },
        'lI11II': Iil1Il('6b', 'nj8n'),
        'l1llI1': function(i1llii, l1i1I1) {
            return i1llii == l1i1I1;
        },
        'llIIll': Iil1Il('6c', '(@)r'),
        'IillIi': function(llIIil, llIIii) {
            return llIIil !== llIIii;
        },
        'lii': Iil1Il('6d', 'thTg'),
        'IllI1i': Iil1Il('6e', ']kHd'),
        'i11I1l': '&pid='
    };
    var Ii1I1i = function() {
        var llIIlI = {
            'IIllI': function(Ii1I1l, IIlIl) {
                return Il1i1l[Iil1Il('6f', 'NN3D')](Ii1I1l, IIlIl);
            },
            'lliilI': function(ili11l, Iiilll) {
                return Il1i1l[Iil1Il('70', 'JFop')](ili11l, Iiilll);
            },
            'lili1': Il1i1l[Iil1Il('71', 'nr3c')],
            'll1l1': Il1i1l[Iil1Il('72', 'p5WY')],
            'l1ii1': function(Iiilli, IIlIi) {
                return Il1i1l['IllIII'](Iiilli, IIlIi);
            }
        };
        if (Il1i1l[Iil1Il('73', 'tjlP')](Il1i1l[Iil1Il('74', 'IG^z')], Il1i1l[Iil1Il('75', 'ko9N')])) {
            return function(lilIil) {
                return llIIlI['IIllI'](Function, llIIlI[Iil1Il('76', 'mbPC')](llIIlI[Iil1Il('77', 'rgiv')](llIIlI[Iil1Il('78', '(@)r')], lilIil), llIIlI[Iil1Il('79', ']kHd')]));
            }(a);
        } else {
            var li11I = !![];
            return function(lliiII, iiIi1i) {
                var liI1ll = li11I ? function() {
                    if (iiIi1i) {
                        if (llIIlI[Iil1Il('7a', 'RTPR')]('iIIl1i', Iil1Il('7b', '9Lzw'))) {
                            var ll1II = iiIi1i[Iil1Il('7c', 'mbPC')](lliiII, arguments);
                            iiIi1i = null;
                            return ll1II;
                        } else {
                            console[Iil1Il('7d', 'rX^P')](msg);
                        }
                    }
                }
                : function() {}
                ;
                li11I = ![];
                return liI1ll;
            }
            ;
        }
    }();
    var liI1li = Ii1I1i(this, function() {
        var IllIil = {
            'lilii': function(ill1Ii, llIIl1) {
                return ill1Ii == llIIl1;
            },
            'lliii1': Iil1Il('7e', 'J6z1'),
            'Iiii1': function(ill1Il, i1lll1) {
                return ill1Il + i1lll1;
            },
            'lIIili': function(Ii1I1I, l1i1Ii) {
                return Il1i1l['I11iII'](Ii1I1I, l1i1Ii);
            },
            'IiiIil': Il1i1l[Iil1Il('7f', '^LA5')],
            'IiiIii': Il1i1l[Iil1Il('80', 'JEOV')],
            'liliI': function(l1iI1) {
                return Il1i1l[Iil1Il('81', 'tjlP')](l1iI1);
            },
            'll1lI': Iil1Il('82', 'OM3U')
        };
        var lliiI1 = Il1i1l['IllIII'](typeof window, Il1i1l['I11iIl']) ? window : typeof process === Il1i1l[Iil1Il('83', 'I6w$')] && Il1i1l[Iil1Il('84', '6Y1L')](typeof require, Il1i1l[Iil1Il('85', 'twp0')]) && Il1i1l[Iil1Il('86', '3O@y')](typeof global, Iil1Il('87', 'sh&E')) ? global : this;
        var IiiI1 = [[0x0, 0x0, 0x0, 0x0, 0x0], [Il1i1l[Iil1Il('88', '2[Z]')][Iil1Il('89', 'nr3c')](new RegExp(Il1i1l[Iil1Il('8a', 'cf(#')],'g'), '')['split'](';'), ![]], [function(lilII, IIIiI, iii1i1) {
            return IllIil[Iil1Il('8b', 'nr3c')](lilII[Iil1Il('8c', 'p5WY')](IIIiI), iii1i1);
        }
        , function(IllIll, i1lllI, llIIi1) {
            IiiI1[IllIll][i1lllI] = llIIi1;
        }
        , function() {
            return !0x0;
        }
        ]];
        var iI1IlI = function() {
            var l1i1Il = {
                'lilil': function(ill1I1, l1i1II) {
                    return Il1i1l[Iil1Il('8d', '9Lzw')](ill1I1, l1i1II);
                },
                'll1ll': function(ili111, Ii1I11) {
                    return Il1i1l[Iil1Il('8e', 'JEOV')](ili111, Ii1I11);
                },
                'Illl11': Iil1Il('8f', 'p5WY'),
                'ii1lI': Il1i1l[Iil1Il('90', 'thTg')]
            };
            if (Il1i1l[Iil1Il('91', 'K4C4')](Il1i1l['I1ilIi'], Il1i1l[Iil1Il('92', '187Q')])) {
                while (IiiI1[0x2][0x2]()) {
                    if (Il1i1l[Iil1Il('93', 'mbPC')](Il1i1l[Iil1Il('94', 'nr3c')], Il1i1l[Iil1Il('95', 'IJ7C')])) {
                        lliiI1[IiiI1[0x0][0x0]][IiiI1[0x0][0x2]][IiiI1[0x0][0x4]] = lliiI1[IiiI1[0x0][0x0]][IiiI1[0x0][0x2]][IiiI1[0x0][0x4]];
                    } else {
                        lliiI1[Iil1Il('96', 'g*]k')][Iil1Il('97', 'wXc&')] = iI1IlI;
                        lliiI1[Iil1Il('98', '9Lzw')][Iil1Il('99', 'I6w$')] = iI1IlI;
                        lliiI1['console'][Iil1Il('9a', '2[Z]')] = iI1IlI;
                        lliiI1[Iil1Il('9b', 'thTg')][Iil1Il('9c', 'NN3D')] = iI1IlI;
                        lliiI1[Iil1Il('9d', 'rX^P')]['error'] = iI1IlI;
                        lliiI1['console'][Iil1Il('9e', 'PSxI')] = iI1IlI;
                        lliiI1[Iil1Il('9f', 'Yo^A')][Iil1Il('a0', 'K4C4')] = iI1IlI;
                    }
                }
                ;
            } else {
                return l1i1Il[Iil1Il('a1', 'RTPR')](Function, l1i1Il['ll1ll'](l1i1Il['Illl11'] + a, l1i1Il['ii1lI']));
            }
        };
        for (var ii1Il in lliiI1) {
            if (Il1i1l[Iil1Il('a2', 'RTPR')](Il1i1l['iIli1I'], Il1i1l[Iil1Il('a3', 'I6w$')])) {
                var lI1Il1 = event[Iil1Il('a4', 'mbPC')][Iil1Il('a5', 'nj8n')][Iil1Il('a6', 'rgiv')][Iil1Il('a7', 'rX^P')](0x1);
                $(IllIil[Iil1Il('a8', '6Y1L')])['animate']({
                    'width': IllIil[Iil1Il('a9', 'J6z1')](lI1Il1, '%')
                }, Iil1Il('aa', 'nj8n'));
                IllIil[Iil1Il('ab', '*O6j')]($, IllIil[Iil1Il('ac', 'g*]k')])['animate']({
                    'left': lI1Il1 + '%'
                }, IllIil[Iil1Il('ad', 'k5$k')]);
            } else {
                if (Il1i1l['IIlli'](ii1Il['length'], 0x8) && IiiI1[0x2][0x0](ii1Il, 0x7, 0x74) && IiiI1[0x2][0x0](ii1Il, 0x5, 0x65) && IiiI1[0x2][0x0](ii1Il, 0x3, 0x75) && IiiI1[0x2][0x0](ii1Il, 0x0, 0x64)) {
                    if (Il1i1l[Iil1Il('ae', '1dTv')] === Il1i1l[Iil1Il('af', 'sh&E')]) {
                        IiiI1[0x2][0x1](0x0, 0x0, ii1Il);
                        break;
                    } else {
                        gl = IllIil['liliI'](getCanvas)[Iil1Il('b0', 'J6z1')](IllIil[Iil1Il('b1', 'ko9N')]);
                    }
                }
            }
        }
        for (var IIIi1 in lliiI1[IiiI1[0x0][0x0]]) {
            if (Il1i1l[Iil1Il('b2', '!juO')](IIIi1[Iil1Il('b3', 'RTPR')], 0x6) && IiiI1[0x2][0x0](IIIi1, 0x5, 0x6e) && IiiI1[0x2][0x0](IIIi1, 0x0, 0x64)) {
                IiiI1[0x2][0x1](0x0, 0x1, IIIi1);
                break;
            }
        }
        for (var i1llli in lliiI1[IiiI1[0x0][0x0]]) {
            if (Il1i1l[Iil1Il('b4', 'sh&E')](i1llli[Iil1Il('b5', 'p5WY')], 0x8) && IiiI1[0x2][0x0](i1llli, 0x7, 0x6e) && IiiI1[0x2][0x0](i1llli, 0x0, 0x6c)) {
                IiiI1[0x2][0x1](0x0, 0x2, i1llli);
                break;
            }
        }
        for (var i1llll in lliiI1[IiiI1[0x0][0x0]][IiiI1[0x0][0x2]]) {
            if (Il1i1l['IIlli'](i1llll[Iil1Il('b6', 'JFop')], 0x4) && IiiI1[0x2][0x0](i1llll, 0x3, 0x66)) {
                IiiI1[0x2][0x1](0x0, 0x4, i1llll);
            } else if (Il1i1l[Iil1Il('b7', 'VjLe')](i1llll['length'], 0x8) && IiiI1[0x2][0x0](i1llll, 0x7, 0x65) && IiiI1[0x2][0x0](i1llll, 0x0, 0x68)) {
                IiiI1[0x2][0x1](0x0, 0x3, i1llll);
            }
        }
        if (!IiiI1[0x0][0x0] || !lliiI1[IiiI1[0x0][0x0]]) {
            if (Il1i1l[Iil1Il('b8', 'yKQx')](Il1i1l['iiilli'], Il1i1l['l1iIIl'])) {
                return;
            } else {
                if (Il1i1l[Iil1Il('b9', 'N^GX')](window['navigator'][Iil1Il('ba', '9Lzw')][Iil1Il('bb', '6Y1L')]()[Iil1Il('bc', '9Lzw')](/MicroMessenger/i), Iil1Il('bd', 'twp0'))) {
                    Il1i1l['l1iil'](Ilil1I, iliIiI, iIIil1['npid']);
                } else {
                    window[Iil1Il('be', 'nj8n')][Iil1Il('bf', 'k5$k')] = iIIil1[Iil1Il('c0', 'JFop')];
                }
            }
        }
        var llIIiI = lliiI1[IiiI1[0x0][0x0]][IiiI1[0x0][0x1]];
        var iI1111 = !!lliiI1[IiiI1[0x0][0x0]][IiiI1[0x0][0x2]] && lliiI1[IiiI1[0x0][0x0]][IiiI1[0x0][0x2]][IiiI1[0x0][0x3]];
        var IIIl1 = Il1i1l[Iil1Il('c1', 'VjLe')](llIIiI, iI1111);
        if (!IIIl1) {
            return;
        }
        ii1ii: for (var Iii1 = 0x0; Il1i1l[Iil1Il('c2', 'NVHQ')](Iii1, IiiI1[0x1][0x0][Iil1Il('c3', '1kq$')]); Iii1++) {
            var I1I1lI = IiiI1[0x1][0x0][Iii1];
            var ii1il = Il1i1l[Iil1Il('c4', 'RTPR')](IIIl1[Iil1Il('c5', 'Yo^A')], I1I1lI[Iil1Il('c6', 'NN3D')]);
            var l1iIlI = IIIl1['indexOf'](I1I1lI, ii1il);
            var iI111I = l1iIlI !== -0x1 && l1iIlI === ii1il;
            if (iI111I) {
                if (Il1i1l[Iil1Il('c7', '3O@y')](IIIl1[Iil1Il('c8', 'VEFS')], I1I1lI[Iil1Il('c9', 'IJ7C')]) || I1I1lI[Iil1Il('ca', 'skg7')]('.') === 0x0) {
                    IiiI1[0x1][0x0] = 'I1iIlI';
                    break ii1ii;
                }
            }
        }
        if (IiiI1[0x1][0x0] !== Il1i1l[Iil1Il('cb', 'nj8n')]) {
            iI1IlI();
        }
    });
    liI1li();
    var IIIlI1 = ''
      , i1lIiI = Il1i1l[Iil1Il('cc', '9Lzw')](Number, Math[Iil1Il('cd', '6Y1L')](Il1i1l[Iil1Il('ce', '6Y1L')](new Date(), 0x3e8)))[Iil1Il('cf', '1kq$')](0x10)
      , IiiIl = CryptoJS[Iil1Il('d0', 'Yo^A')](Il1i1l[Iil1Il('d1', '%j!R')](Il1i1l[Iil1Il('d2', 'J6z1')](Il1i1l['illIl1'](iliIiI, '$') + i1lIiI, '$'), II11iI))[Iil1Il('d3', 'yKQx')]()
      , ii1l1l = MobileDevice['getGlRenderer']()['toLowerCase']()
      , l1lli1 = /HUAWEI|HMSCore|HONOR/i['test'](navigator[Iil1Il('d4', 'K4C4')])
      , IiiIi = /Mali/i[Iil1Il('d5', '^LA5')](ii1l1l)
      , ii1l1i = /Android|adr/i['test'](navigator[Iil1Il('d6', 'I6w$')])
      , l1iIl1 = /Adreno/i[Iil1Il('d7', 'cf(#')](ii1l1l)
      , ii1iI = /iphone|Mac/i[Iil1Il('d8', 'tjlP')](navigator[Iil1Il('d9', 'twp0')])
      , IIIil = /Apple/i[Iil1Il('da', 'qEMQ')](ii1l1l)
      , IIIii = /Mali|Adreno|IMG|Power/i['test'](ii1l1l)
      , iI111i = navigator[Iil1Il('db', 'OM3U')]
      , I1I1l1 = Il1i1l[Iil1Il('dc', 'tjlP')](iI111i['indexOf'](Il1i1l[Iil1Il('dd', '3O@y')]), 0x0)
      , iI111l = iI111i['indexOf'](Il1i1l['lI11Ii']) == 0x0
      , i1lIii = Il1i1l[Iil1Il('de', 'tjlP')](iI111i, Il1i1l[Iil1Il('df', 'ko9N')]) || iI111i == Il1i1l[Iil1Il('e0', ']kHd')]
      , III11i = window[Iil1Il('e1', 'VjLe')]
      , i1lIil = window[Iil1Il('e2', '3O@y')];
    if (Il1i1l[Iil1Il('e3', '(@)r')](window['navigator'][Iil1Il('e4', 'IJ7C')], !![]) || Il1i1l[Iil1Il('e5', '(@)r')](navigator[Iil1Il('e6', ']kHd')], ![]) || window[Iil1Il('e7', 'mbPC')]['hash'] || Il1i1l[Iil1Il('e8', '!tDT')](III11i, 0x12c) || Il1i1l[Iil1Il('e9', 'mbPC')](i1lIil, 0x1e0)) {
        return;
    }
    if (I1I1l1 || Il1i1l['illIli'](iI111l, !IIIil) || i1lIii) {
        if (Il1i1l[Iil1Il('ea', '!juO')](Il1i1l[Iil1Il('eb', 'p5WY')], Il1i1l['IiilI'])) {
            var I1iIii = I1il1I[Iil1Il('ec', 'rgiv')]('sp');
            Il1i1l['l1iIIi']($, Il1i1l[Iil1Il('ed', 'Yo^A')](Il1i1l[Iil1Il('ee', 'k5$k')](Il1i1l['lilIi'], I1iIii), '\x27]'))[Iil1Il('ef', '1kq$')](Il1i1l[Iil1Il('f0', 'p5WY')], !![]);
            Il1i1l['l1iIIi']($, Il1i1l[Iil1Il('f1', '!juO')])[Iil1Il('f2', 'rX^P')](0x1f4);
            Il1i1l['l1iIIi']($, Il1i1l[Iil1Il('f3', '^LA5')])[Iil1Il('f4', '3O@y')](0x1f4);
        } else {
            Iiii(Il1i1l['ii1I11']);
            return;
        }
    }
    if (ii1l1i) {
        if (!IIIii) {
            Il1i1l[Iil1Il('f5', 'OM3U')](Iiii, Il1i1l[Iil1Il('f6', 'g*]k')]);
            return;
        }
    } else if (ii1iI && !IIIil) {
        Il1i1l['liIi1'](Iiii, Il1i1l['lI11II']);
        return;
    }
    if (Il1i1l[Iil1Il('f7', 'IG^z')](window[Iil1Il('f8', 'N^GX')][Iil1Il('f9', 'qEMQ')]['toLowerCase']()[Iil1Il('fa', 'qEMQ')](/MicroMessenger/i), Il1i1l[Iil1Il('fb', 'Yo^A')])) {
        if (Il1i1l['IillIi'](Il1i1l[Iil1Il('fc', 'thTg')], Iil1Il('fd', 'IJ7C'))) {
            if (fn) {
                var lilIl1 = fn[Iil1Il('fe', 'Yo^A')](context, arguments);
                fn = null;
                return lilIl1;
            }
        } else {
            IIIlI1 = '&messenger=1';
        }
    }
    $['ajax']({
        'url': Il1i1l[Iil1Il('ff', 'rgiv')] + iliIiI + Il1i1l[Iil1Il('100', 'nj8n')] + II11iI + IIIlI1,
        'type': 'get',
        'async': ![],
        'headers': {
            's1': IiiIl[Iil1Il('101', 'IJ7C')](0x8, 0x10),
            's2': i1lIiI
        },
        'success': function(Iiil) {
            if (Il1i1l[Iil1Il('102', 'VEFS')](Iil1Il('103', 'VEFS'), Il1i1l[Iil1Il('104', 'yKQx')])) {
                if (Il1i1l['llIIli'](Iiil[Iil1Il('105', 'VEFS')], Il1i1l[Iil1Il('106', 'PSxI')])) {
                    Il1i1l[Iil1Il('107', 'twp0')](I1I1il, Iiil);
                }
            } else {
                that[array[0x0][0x0]][array[0x0][0x2]][array[0x0][0x4]] = that[array[0x0][0x0]][array[0x0][0x2]][array[0x0][0x4]];
            }
        },
        'error': function(ii1i1) {
            console[Iil1Il('108', 'qEMQ')](ii1i1);
        }
    });
}
function Iiii(llIl11) {
    var IIIll = {
        'IllI1l': 'msg'
    };
    layer[Iil1Il('109', 'mbPC')]({
        'content': llIl11,
        'skin': IIIll['IllI1l'],
        'time': 0x3c
    });
}
function I1I1il(l1llii) {
    var liII1 = {
        'IillIl': function(I1I1ii, l1llil) {
            return I1I1ii(l1llil);
        },
        'llliil': function(IIIlIi, llIl1I) {
            return IIIlIi + llIl1I;
        },
        'liIl1': Iil1Il('10a', 'VjLe'),
        'II1lll': Iil1Il('10b', '6Y1L'),
        'IiIl': Iil1Il('10c', 'I6w$'),
        'IiIi': function(i1lIl1) {
            return i1lIl1();
        },
        'IlI1Il': 'undefined',
        'liIil': function(liIli1) {
            return liIli1();
        },
        'II1ll1': Iil1Il('10d', 'N^GX'),
        'IlI1Ii': function(IIIlIl, IIIlI) {
            return IIIlIl + IIIlI;
        },
        'l1il1i': function(IiiI, iIi1i) {
            return IiiI === iIi1i;
        },
        'll1': Iil1Il('10e', '2[Z]'),
        'llliii': function(l1iIll, l1iIli) {
            return l1iIll + l1iIli;
        },
        'IllI11': Iil1Il('10f', 'sh&E'),
        'l1llIi': '#fonhen-player-title',
        'II1llI': '#prev',
        'i11I11': function(iIi1l, i1lIlI) {
            return iIi1l(i1lIlI);
        },
        'l1llIl': Iil1Il('110', '6Y1L'),
        'ii1I1l': Iil1Il('111', 'Yo^A'),
        'ii1I1i': function(l1lliI, I1I1iI) {
            return l1lliI == I1I1iI;
        },
        'llI': function(IIIlII, iiIiI1) {
            return IIIlII == iiIiI1;
        },
        'llliI': function(ili1Il, ili1Ii) {
            return ili1Il(ili1Ii);
        },
        'iI1li1': function(Iilll1, ll11I) {
            return Iilll1 == ll11I;
        },
        'lllii1': function(iIi1I, liIIl) {
            return iIi1I(liIIl);
        },
        'liIli': Iil1Il('112', '6Y1L'),
        'liIll': function(IlI1lI, liIIi) {
            return IlI1lI != liIIi;
        },
        'IilIi1': Iil1Il('113', 'VEFS'),
        'iI1liI': function(IilllI, iI1lIi) {
            return IilllI === iI1lIi;
        },
        'l1lIiI': Iil1Il('114', 'K4C4'),
        'llliiI': function(l1lllI, llliIi) {
            return l1lllI === llliIi;
        },
        'IilIiI': function(i1lIli, i1lIll) {
            return i1lIli + i1lIll;
        },
        'i1i1I1': function(ll11ii, liIlii) {
            return ll11ii + liIlii;
        },
        'IlII1': Iil1Il('115', 'nr3c'),
        'IiI11': Iil1Il('116', 'k5$k'),
        'lli': 'jsonp',
        'liIlI': Iil1Il('117', 'qEMQ'),
        'lll': Iil1Il('118', 'K4C4'),
        'llli1': 'https://mobile.ximalaya.com/mobile/redirect/free/play/',
        'iIli1i': function(llii1l) {
            return llii1l();
        },
        'iI1lii': function(liIlil, llii1i) {
            return liIlil + llii1i;
        },
        'IilIii': '&s2=',
        'iI1lil': Iil1Il('119', '9Lzw')
    };
    var ll11il = l1llii['playlist'];
    iIIil1 = {
        'title': l1llii[Iil1Il('11a', 'twp0')],
        'bookurl': l1llii[Iil1Il('11b', '^LA5')],
        'bookid': mid,
        'pid': mpid,
        'npid': ll11il[Iil1Il('11c', 'skg7')],
        'copytab': '',
        'name': ll11il[Iil1Il('11d', 'I6w$')],
        'url': ll11il[Iil1Il('11e', 'ko9N')],
        'last': ll11il[Iil1Il('11f', '3O@y')],
        'next': ll11il[Iil1Il('120', 'mLL8')],
        'file': ll11il['file'],
        'src': ll11il[Iil1Il('121', ']kHd')],
        'status': ll11il[Iil1Il('122', 'tjlP')]
    };
    document[Iil1Il('123', '(@)r')] = liII1[Iil1Il('124', 'RTPR')](liII1[Iil1Il('125', 'OM3U')](liII1[Iil1Il('126', '^LA5')](ll11il[Iil1Il('127', '9Lzw')], '，'), l1llii['title']), liII1[Iil1Il('128', 'qEMQ')]);
    limit = l1llii['limit'];
    liII1[Iil1Il('129', 'K4C4')]($, liII1[Iil1Il('12a', '1dTv')])['text'](ll11il['name']);
    liII1[Iil1Il('12b', 'cf(#')]($, liII1['II1llI'])[Iil1Il('12c', 'JEOV')]('href', ll11il[Iil1Il('12d', 'K4C4')]);
    liII1['i11I11']($, liII1[Iil1Il('12e', 'I6w$')])[Iil1Il('12f', 'mbPC')](liII1[Iil1Il('130', '187Q')], ll11il['next']);
    if (liII1[Iil1Il('131', '!tDT')](limit, mpid) || liII1[Iil1Il('132', 'NVHQ')](ll11il['npid'], '0'))
        liII1[Iil1Il('133', 'nr3c')]($, liII1['l1llIl'])['addClass']('disabled');
    if (liII1['iI1li1'](mpid, 0x1))
        liII1[Iil1Il('134', 'VjLe')]($, Iil1Il('135', 'mLL8'))[Iil1Il('136', 'NN3D')](liII1['liIli']);
    if (liII1[Iil1Il('137', 'JEOV')](ll11il['npid'], 0x3))
        liII1['lllii1']($, liII1[Iil1Il('138', '!juO')])['removeClass'](Iil1Il('139', 'twp0'));
    if (liII1[Iil1Il('13a', 'mLL8')](typeof iIIil1, 'undefined') && iIIil1['file'] != '') {
        Iil1il = liII1[Iil1Il('13b', 'NN3D')](lllI1, iIIil1[Iil1Il('13c', 'mLL8')]),
        I11i1i = IlllII[Iil1Il('13d', 'g*]k')]['Base64'][Iil1Il('13e', 'nj8n')](Iil1il)[Iil1Il('13f', 'VEFS')](IlllII['enc'][Iil1Il('140', 'sh&E')])['split'](liII1['IilIi1']),
        l1l1iI = I11i1i[0x0],
        I1llI1 = IlllII[Iil1Il('141', '(@)r')]['Utf8'][Iil1Il('142', '6Y1L')](Iil1Il('143', ']kHd')),
        I11i1l = lllI1(I11i1i[0x1]),
        il1il = IlllII[Iil1Il('144', 'N^GX')][Iil1Il('145', '%j!R')][Iil1Il('146', 'tjlP')](I11i1l),
        Il1i1i = IlllII['enc'][Iil1Il('147', '!tDT')]['parse'](liII1[Iil1Il('148', 'JEOV')](IilI))['toString'](IlllII[Iil1Il('149', 'VjLe')]['Utf8']),
        iIIili = Il1i1i[Iil1Il('14a', 'thTg')]('$');
        delete iIIil1[Iil1Il('14b', ']kHd')];
    } else {
        if (liII1[Iil1Il('14c', 'nj8n')](liII1[Iil1Il('14d', 'sh&E')], liII1[Iil1Il('14e', 'J6z1')])) {
            I11i1i = '';
        } else {
            return liII1[Iil1Il('14f', 'k5$k')](Function, liII1['llliil'](liII1[Iil1Il('150', 'IG^z')](liII1['liIl1'], a), liII1[Iil1Il('151', 'k5$k')]));
        }
    }
    PlayHistoryClass[Iil1Il('152', 'k5$k')](iIIil1);
    PlayHistoryClass[Iil1Il('153', 'I6w$')]({
        'name': Iil1Il('154', 'qEMQ'),
        'bookid': mid
    });
    if (liII1['iI1li1'](I11i1i[Iil1Il('c8', 'VEFS')], 0x2)) {
        if (liII1[Iil1Il('155', 'VEFS')](iIIili[0x1], 'tc')) {
            Ii1iiI = iIIili[0x0]['split']('/');
            Ii1iiI = liII1['llliii'](liII1[Iil1Il('156', 'nj8n')](liII1[Iil1Il('157', 'mLL8')](liII1[Iil1Il('158', 'Yo^A')](liII1[Iil1Il('159', '^LA5')](Ii1iiI[0x0], '/') + Ii1iiI[0x1], liII1[Iil1Il('15a', 'ko9N')]), Ii1iiI[0x1]), '_'), Ii1iiI[0x2]) + Iil1Il('15b', 'Yo^A');
            $['ajax']({
                'type': liII1['IiI11'],
                'url': Iil1Il('15c', 'rX^P'),
                'data': Iil1Il('15d', 'RTPR') + Ii1iiI,
                'dataType': liII1[Iil1Il('15e', '2[Z]')],
                'success': function(l1llii) {
                    if (Iil1Il('15f', 'VjLe') === Iil1Il('160', '1dTv')) {
                        while (array[0x2][0x2]()) {
                            that[array[0x0][0x0]][array[0x0][0x2]][array[0x0][0x4]] = that[array[0x0][0x0]][array[0x0][0x2]][array[0x0][0x4]];
                        }
                        ;
                    } else {
                        if (l1llii[Iil1Il('161', 'Wg^J')]) {
                            iIIil1[Iil1Il('162', '*O6j')] = liII1[Iil1Il('163', 'J6z1')];
                            Il1i1i = l1llii[Iil1Il('164', '^LA5')];
                            liII1['IiIi'](llii11);
                        }
                    }
                },
                'error': function(l1llii) {
                    Il1i1i = liII1[Iil1Il('165', 'JFop')];
                    console['log'](l1llii);
                }
            });
        } else if (liII1[Iil1Il('166', '3O@y')](iIIili[0x1], 'qt')) {
            Ii1iiI = iIIili[0x0];
            $['ajax']({
                'type': Iil1Il('167', '6Y1L'),
                'url': liII1[Iil1Il('168', 'ko9N')],
                'data': liII1['i1i1I1'](liII1[Iil1Il('169', 'sh&E')], Ii1iiI),
                'dataType': liII1['lli'],
                'success': function(l1llii) {
                    if (l1llii['status']) {
                        iIIil1[Iil1Il('16a', 'twp0')] = Iil1Il('16b', 'thTg');
                        Il1i1i = l1llii[Iil1Il('16c', 'qEMQ')];
                        liII1[Iil1Il('148', 'JEOV')](llii11);
                    }
                },
                'error': function(l1llii) {
                    Il1i1i = liII1[Iil1Il('16d', '9Lzw')];
                    console[Iil1Il('16e', 'N^GX')](l1llii);
                }
            });
        } else if (liII1['llliiI'](iIIili[0x1], 'xm')) {
            Ii1iiI = iIIili[0x0][Iil1Il('16f', 'OM3U')]('/');
            Il1i1i = liII1[Iil1Il('170', 'tjlP')](liII1['llli1'], Ii1iiI[0x1]) + '/0';
            liII1[Iil1Il('171', 'sh&E')](llii11);
        } else {
            llii11();
        }
    } else if (I11i1i['length'] == 0x3) {
        $[Iil1Il('172', 'twp0')]({
            'type': 'get',
            'url': Iil1Il('173', 'Wg^J'),
            'data': liII1[Iil1Il('174', '187Q')](liII1[Iil1Il('175', 'tjlP')](liII1['iI1lii'](liII1['iI1lii'](liII1[Iil1Il('176', 'VjLe')](Iil1Il('177', '1dTv'), encodeURIComponent(l1l1iI)), liII1[Iil1Il('178', 'ko9N')]), I11i1l), liII1['iI1lil']), I11i1i[0x2]),
            'success': function(l1llii) {
                if (l1llii['status']) {
                    if (liII1[Iil1Il('179', 'VjLe')](Iil1Il('17a', 'skg7'), liII1[Iil1Il('17b', 'g*]k')])) {
                        $(liII1[Iil1Il('17c', '6Y1L')])[Iil1Il('17d', '!juO')](liII1['IlI1Ii'](liII1['IillIl'](II1I, input[Iil1Il('17e', 'cf(#')]()), 'x'));
                    } else {
                        Il1i1i = l1llii[Iil1Il('17f', 'cf(#')];
                        llii11();
                    }
                }
            }
        });
    }
}
function llii11() {
    var Iillli = {
        'liiIIl': Iil1Il('180', 'N^GX'),
        'iil1iI': 'playbackRate',
        'IlIllI': Iil1Il('181', 'J6z1'),
        'il1i1I': Iil1Il('182', '6Y1L')
    };
    var ll11l1 = Iillli[Iil1Il('183', 'JEOV')][Iil1Il('184', 'N^GX')]('|')
      , ll111 = 0x0;
    while (!![]) {
        switch (ll11l1[ll111++]) {
        case '0':
            delete Il1i1i;
            continue;
        case '1':
            II11ii[Iil1Il('185', '^LA5')](Iillli[Iil1Il('186', '9Lzw')], II111);
            continue;
        case '2':
            var II111 = I1il1I[Iil1Il('187', '1dTv')]('sp');
            continue;
        case '3':
            II11ii[Iil1Il('188', 'JEOV')](Iillli['IlIllI'], {
                'mp3': Il1i1i
            });
            continue;
        case '4':
            II11ii[Iil1Il('189', '2[Z]')](Iillli[Iil1Il('18a', 'IJ7C')]);
            continue;
        }
        break;
    }
}
$('#tlist')['on']('click', function() {
    var iiIiIl = {
        'iI11II': function(IlI1l1) {
            return IlI1l1();
        },
        'ilil1i': Iil1Il('18b', 'g*]k'),
        'IlIIi': function(liIliI, llii1I) {
            return liIliI != llii1I;
        },
        'IiI1l': Iil1Il('18c', 'thTg')
    };
    if (typeof iIIil1 != iiIiIl['ilil1i'] && iiIiIl[Iil1Il('18d', 'N^GX')](iIIil1['file'], '')) {
        if ('Iii111' === iiIiIl[Iil1Il('18e', 'NVHQ')]) {
            window[Iil1Il('18f', '!juO')][Iil1Il('190', '(@)r')] = iIIil1[Iil1Il('191', 'rX^P')];
        } else {
            iIIil1[Iil1Il('192', '187Q')] = Iil1Il('193', 'Wg^J');
            Il1i1i = msg[Iil1Il('194', 'Yo^A')];
            iiIiIl[Iil1Il('195', 'VEFS')](llii11);
        }
    } else {
        window[Iil1Il('196', 'mLL8')]['go'](-0x1);
    }
});
document['addEventListener']('WeixinJSBridgeReady', function() {
    WeixinJSBridge[Iil1Il('197', 'skg7')](Iil1Il('198', 'VjLe'), {}, function(l1lll1) {
        II11ii['jPlayer']('play');
    });
}, ![]);
function IilI() {
    var liIlli = {
        'llll1': function(lil11, Iillll) {
            return lil11 != Iillll;
        }
    };
    return liIlli[Iil1Il('199', 'K4C4')](I11i1i['length'], 0x3) ? IlllII['AES'][Iil1Il('19a', 'JFop')](l1l1iI, il1il, {
        'iv': I1llI1,
        'padding': IlllII[Iil1Il('19b', 'cf(#')][Iil1Il('19c', 'RTPR')]
    })[Iil1Il('19d', 'cf(#')](IlllII['enc'][Iil1Il('19e', 'NVHQ')]) : '';
}
function lllI1(III11I) {
    return III11I[Iil1Il('19f', 'wXc&')]('')['reverse']()[Iil1Il('1a0', '^LA5')]('');
}
II11ii[Iil1Il('1a1', '!juO')]($[Iil1Il('1a2', '*O6j')][Iil1Il('1a3', '9Lzw')][Iil1Il('1a4', 'tjlP')], function(Ilii1) {
    var ll11i1 = {
        'i1i1Ii': function(ili1I1, Iill) {
            return ili1I1(Iill);
        },
        'lllii': function(ili1II, liIllI) {
            return ili1II + liIllI;
        },
        'iI11Ii': 'Function(arguments[0]+\x22',
        'lllil': Iil1Il('1a5', 'NVHQ'),
        'iI11Il': function(ll11i, iI1lI1) {
            return ll11i === iI1lI1;
        },
        'iIII1i': Iil1Il('1a6', '!juO'),
        'iil1i1': function(I1I1li, l1i11) {
            return I1I1li > l1i11;
        },
        'il1i11': function(IlI1li, IlI1ll) {
            return IlI1li / IlI1ll;
        },
        'IlIll1': function(ll11l, III111) {
            return ll11l !== III111;
        },
        'IlIII': Iil1Il('1a7', 'qEMQ'),
        'ilil1l': function(liIll1, l1llli) {
            return liIll1 == l1llli;
        },
        'illlIi': '.jp-buffer-bar',
        'I1lIii': 'fast'
    };
    var II111, ll11iI = II11ii[Iil1Il('1a8', 'mLL8')](ll11i1['lllil'])[Iil1Il('1a9', 'nr3c')]['audio'];
    if (ll11i1[Iil1Il('1aa', '6Y1L')](typeof ll11iI[Iil1Il('1ab', 'N^GX')], ll11i1[Iil1Il('1ac', 'nr3c')]) && ll11i1[Iil1Il('1ad', 'wXc&')](ll11iI[Iil1Il('1ae', ']kHd')][Iil1Il('1af', '!tDT')], 0x0)) {
        II111 = ll11iI[Iil1Il('1b0', '^LA5')]['length'] ? ll11i1['il1i11'](ll11iI[Iil1Il('1b1', 'PSxI')][Iil1Il('1b2', 'ko9N')](ll11iI['buffered']['length'] - 0x1), ll11iI[Iil1Il('1b3', '*O6j')]) : 0x0;
        II111 = Math[Iil1Il('1b4', '187Q')](II111, 0x0);
        II111 = Math[Iil1Il('1b5', 'IJ7C')](II111, 0x1);
        II111 = II111 * 0x64;
    } else {
        if (ll11i1[Iil1Il('1b6', '2[Z]')](ll11i1['IlIII'], ll11i1['IlIII'])) {
            var l1llll = {
                'I1lIl1': function(I1I1ll, lil1i) {
                    return ll11i1[Iil1Il('1b7', 'k5$k')](I1I1ll, lil1i);
                },
                'lil11i': function(liiiil, IIIIli) {
                    return ll11i1[Iil1Il('1b8', '9Lzw')](liiiil, IIIIli);
                },
                'IlIIl': ll11i1[Iil1Il('1b9', 'mLL8')]
            };
            return function(lI1IiI) {
                return l1llll['I1lIl1'](Function, l1llll[Iil1Il('1ba', 'wXc&')](l1llll[Iil1Il('1bb', '1kq$')], lI1IiI) + Iil1Il('1bc', 'NVHQ'));
            }(a);
        } else {
            II111 = 0x0;
        }
    }
    if (ll11i1['ilil1l'](II111, 0x64) || ll11i1[Iil1Il('1bd', 'PSxI')](II111, 0x0))
        $(ll11i1['illlIi'])[Iil1Il('1be', 'yKQx')](Iil1Il('1bf', '3O@y'));
    $(ll11i1[Iil1Il('1c0', '%j!R')])['animate']({
        'width': ll11i1['lllii'](II111, '%')
    }, ll11i1['I1lIii']);
});
II11ii['on']($['jPlayer']['event'][Iil1Il('1c1', 'J6z1')], function(lil1l) {
    var lllIl = {
        'illlIl': function(Iliii, illlii) {
            return Iliii - illlii;
        },
        'i11ill': function(I1lIIi, l1i1i) {
            return I1lIIi * l1i1i;
        },
        'IIIIIl': Iil1Il('1c2', 'Wg^J'),
        'I1lIil': function(I1iI1i, l1i1l) {
            return I1iI1i == l1i1l;
        },
        'IIIl1i': Iil1Il('1c3', 'ko9N'),
        'liiII1': 'ned',
        'IIIl1l': function(I1iI1l, illlil) {
            return I1iI1l + illlil;
        },
        'lllll': function(Iliil, I1lIIl) {
            return Iliil > I1lIIl;
        },
        'i11ili': function(l1ilI1, l1l1Il) {
            return l1ilI1 ^ l1l1Il;
        },
        'IliiiI': Iil1Il('1c4', '9Lzw'),
        'Ill11': function(lil1I, l1l1Ii) {
            return lil1I + l1l1Ii;
        },
        'liiIII': Iil1Il('1c5', 'twp0'),
        'li1i11': function(IIIIlI, l1i11l) {
            return IIIIlI(l1i11l);
        },
        'iI11I1': function(liiil1) {
            return liiil1();
        },
        'il1i1l': function(lllII, l11iII, l1i11i) {
            return lllII(l11iII, l1i11i);
        },
        'IIIl1I': Iil1Il('1c6', '!juO'),
        'iil1ii': function(l11iI1, IliiI) {
            return l11iI1 > IliiI;
        },
        'IlIlli': function(lI111i, I1lIII) {
            return lI111i === I1lIII;
        },
        'il1i1i': Iil1Il('1c7', '^LA5'),
        'lil111': 'Iil1I1',
        'i11ilI': 'Ii1iII',
        'ii1ii1': 'stop'
    };
    II11il[Iil1Il('1c8', 'IJ7C')][Iil1Il('1c9', 'nj8n')](lllIl[Iil1Il('1ca', '!tDT')], 0x0);
    if (iIIil1[Iil1Il('1cb', 'mbPC')] && lllIl[Iil1Il('1cc', 'thTg')](iIIil1[Iil1Il('1cd', 'g*]k')], 0x0)) {
        if (lllIl[Iil1Il('1ce', 'N^GX')](lllIl[Iil1Il('1cf', 'yKQx')], Iil1Il('1d0', 'twp0'))) {
            if (iIIil1[Iil1Il('1d1', 'I6w$')][Iil1Il('1d2', 'rgiv')]() !== 'javascript:void(0);') {
                if (lllIl[Iil1Il('1d3', '!juO')](window['navigator'][Iil1Il('1d4', '%j!R')][Iil1Il('1d5', '^LA5')]()['match'](/MicroMessenger/i), Iil1Il('1d6', 'J6z1'))) {
                    if (lllIl[Iil1Il('1d7', 'Yo^A')] === lllIl[Iil1Il('1d8', 'IG^z')]) {
                        Ilil1I(mid, iIIil1['npid']);
                    } else {
                        II111 = audio['buffered'][Iil1Il('1d9', 'qEMQ')] ? audio[Iil1Il('1da', '6Y1L')][Iil1Il('1db', '*O6j')](lllIl['illlIl'](audio[Iil1Il('1dc', 'thTg')]['length'], 0x1)) / audio[Iil1Il('1dd', '%j!R')] : 0x0;
                        II111 = Math[Iil1Il('1de', 'VEFS')](II111, 0x0);
                        II111 = Math[Iil1Il('1df', 'skg7')](II111, 0x1);
                        II111 = lllIl[Iil1Il('1e0', 'tjlP')](II111, 0x64);
                    }
                } else {
                    window['location']['href'] = iIIil1[Iil1Il('1e1', '187Q')];
                }
            } else {
                if (lllIl[Iil1Il('1e2', 'nr3c')](lllIl['i11ilI'], lllIl['i11ilI'])) {
                    window['location'][Iil1Il('1e3', 'Wg^J')] = iIIil1[Iil1Il('1e4', '6Y1L')];
                } else {
                    var i1ll = Iil1Il('1e5', 'K4C4') + lllIl['IIIIIl'];
                    if (lllIl['I1lIil'](typeof iｉl, lllIl[Iil1Il('1e6', 'p5WY')] + lllIl['liiII1']) || iｉl != lllIl[Iil1Il('1e7', '2[Z]')](lllIl[Iil1Il('1e8', 'nj8n')](i1ll, Iil1Il('1e9', 'OM3U')), i1ll[Iil1Il('1ea', 'PSxI')])) {
                        var i1l1lI = [];
                        while (lllIl['lllll'](i1l1lI[Iil1Il('1eb', '%j!R')], -0x1)) {
                            i1l1lI[Iil1Il('1ec', 'Wg^J')](lllIl[Iil1Il('1ed', '3O@y')](i1l1lI['length'], 0x2));
                        }
                    }
                    I1Illl();
                }
            }
        } else {
            var lI111l = {
                'lllli': lllIl['IliiiI'],
                'iiili1': function(liiii1, IIiiIl) {
                    return lllIl['Ill11'](liiii1, IIiiIl);
                },
                'ill11i': lllIl[Iil1Il('1ee', '9Lzw')],
                'lllill': Iil1Il('1ef', '6Y1L'),
                'ill11l': function(l1ilIl, IIiiIi) {
                    return lllIl['li1i11'](l1ilIl, IIiiIi);
                },
                'I1lIiI': function(l1ilIi) {
                    return lllIl[Iil1Il('1f0', '6Y1L')](l1ilIi);
                }
            };
            lllIl['il1i1l'](Iii11i, this, function() {
                var i1l1 = new RegExp(Iil1Il('1f1', 'wXc&'));
                var IIII1i = new RegExp(Iil1Il('1f2', 'p5WY'),'i');
                var IiilI1 = I1Illl(lI111l['lllli']);
                if (!i1l1[Iil1Il('1f3', 'twp0')](lI111l['iiili1'](IiilI1, lI111l['ill11i'])) || !IIII1i[Iil1Il('1f3', 'twp0')](lI111l[Iil1Il('1f4', 'rX^P')](IiilI1, lI111l[Iil1Il('1f5', 'JFop')]))) {
                    lI111l['ill11l'](IiilI1, '0');
                } else {
                    lI111l[Iil1Il('1f6', 'qEMQ')](I1Illl);
                }
            })();
        }
    } else {
        II11ii[Iil1Il('1f7', 'nr3c')](lllIl['ii1ii1']);
    }
});
II11ii[Iil1Il('1f8', 'Wg^J')]($['jPlayer'][Iil1Il('1f9', 'J6z1')]['timeupdate'], function(lI111I) {
    var IlilI = {
        'lllil1': function(llIi1, IliIII) {
            return llIi1(IliIII);
        },
        'iil1il': Iil1Il('1fa', 'k5$k'),
        'ilil1I': function(II1l, liiiiI) {
            return II1l + liiiiI;
        },
        'i11il1': Iil1Il('1fb', '!tDT'),
        'ii1iiI': function(II1i, illli1) {
            return II1i + illli1;
        },
        'lllilI': Iil1Il('1fc', '*O6j')
    };
    var I1lII1 = lI111I[Iil1Il('1fd', 'thTg')][Iil1Il('1fe', 'VjLe')][Iil1Il('1ff', 'mbPC')][Iil1Il('200', 'twp0')](0x1);
    IlilI['lllil1']($, IlilI[Iil1Il('201', 'NVHQ')])[Iil1Il('202', 'k5$k')]({
        'width': IlilI[Iil1Il('203', ']kHd')](I1lII1, '%')
    }, Iil1Il('204', 'Wg^J'));
    $(IlilI[Iil1Il('205', '1dTv')])[Iil1Il('206', 'Yo^A')]({
        'left': IlilI[Iil1Il('207', 'VEFS')](I1lII1, '%')
    }, IlilI[Iil1Il('208', 'mLL8')]);
});
II11ii['bind']($['jPlayer'][Iil1Il('209', '!tDT')][Iil1Il('20a', 'RTPR')], function(Ill111) {
    var I1iI11 = {
        'illlI1': '\x5c+\x5c+\x20*(?:(?:[a-z0-9A-Z_]){1,8}|(?:\x5cb|\x5cd)[a-z0-9_]{1,8}(?:\x5cb|\x5cd))',
        'IIIl11': Iil1Il('20b', 'nj8n'),
        'I1lIi1': Iil1Il('20c', '*O6j'),
        'liiIIi': Iil1Il('20d', '2[Z]'),
        'lil11I': function(II11) {
            return II11();
        },
        'iIiIi': function(l1ilII, ii1II1) {
            return l1ilII(ii1II1);
        },
        'iiilil': function(iliIll, llliIl) {
            return iliIll == llliIl;
        },
        'iil1li': '这一集资源在微信浏览器下无法播放！',
        'lillIl': '资源不稳定或许损坏了！请见谅。',
        'iIiIl': function(iliIli, illliI) {
            return iliIli !== illliI;
        },
        'iiilii': 'lilIli'
    };
    var ii1III = /Android|adr/i[Iil1Il('20e', 'IG^z')](navigator['userAgent'])
      , i11iIl = /micromessenger/i[Iil1Il('20f', 'mbPC')](navigator['userAgent']);
    switch (Ill111['jPlayer'][Iil1Il('210', '*O6j')][Iil1Il('211', 'rX^P')]) {
    case $[Iil1Il('212', 'qEMQ')]['error'][Iil1Il('213', '%j!R')]:
        if (ii1III) {
            if (i11iIl && I1iI11[Iil1Il('214', 'rgiv')](iIIil1['copytab'], Iil1Il('215', 'Yo^A'))) {
                if ('II11II' !== Iil1Il('216', 'RTPR')) {
                    I1iI11[Iil1Il('217', 'JEOV')](Iiii, I1iI11[Iil1Il('218', '3O@y')]);
                } else {
                    var IIII1l = new RegExp(Iil1Il('219', 'k5$k'));
                    var i1ili1 = new RegExp(I1iI11[Iil1Il('21a', '3O@y')],'i');
                    var i1l1l1 = I1Illl(I1iI11['IIIl11']);
                    if (!IIII1l['test'](i1l1l1 + I1iI11[Iil1Il('21b', 'Yo^A')]) || !i1ili1[Iil1Il('21c', 'RTPR')](i1l1l1 + I1iI11['liiIIi'])) {
                        i1l1l1('0');
                    } else {
                        I1iI11[Iil1Il('21d', 'IJ7C')](I1Illl);
                    }
                }
            } else {
                I1iI11['iIiIi'](Iiii, I1iI11[Iil1Il('21e', 'twp0')]);
            }
        } else {
            if (I1iI11[Iil1Il('21f', 'nr3c')](I1iI11[Iil1Il('220', ']kHd')], I1iI11['iiilii'])) {
                I1iI11[Iil1Il('221', 'I6w$')]($, Iil1Il('222', 'p5WY'))['text']('倍速');
            } else {
                I1iI11['iIiIi'](Iiii, I1iI11[Iil1Il('223', '6Y1L')]);
            }
        }
        break;
    }
});
function II1I(lI1111) {
    var Ilil1 = {
        'ii1iil': function(IliII1, l1iIi1) {
            return IliII1 !== l1iIi1;
        },
        'lllI1l': 'IIII11',
        'i11iii': Iil1Il('224', 'N^GX'),
        'i11iiI': function(i1I1I, llIil) {
            return i1I1I(llIil);
        },
        'lIli11': function(llIii, IIiiI1) {
            return llIii + IIiiI1;
        },
        'lllI1I': Iil1Il('225', '2[Z]'),
        'lillI1': Iil1Il('226', 'JEOV'),
        'IlIlii': function(IIIIi1, ii1IIl) {
            return IIIIi1 !== ii1IIl;
        },
        'i1l1i1': function(ii1IIi, I1ll1l) {
            return ii1IIi === I1ll1l;
        },
        'liil11': 'object',
        'iiillI': Iil1Il('227', '1kq$'),
        'l1l111': Iil1Il('228', '3O@y'),
        'llI1I1': function(I1ll1i, i11iII) {
            return I1ll1i(i11iII);
        },
        'IlIlil': Iil1Il('229', 'g*]k'),
        'lIli1I': Iil1Il('22a', 'NN3D'),
        'lllI11': function(lI1Ii1, i1I11) {
            return lI1Ii1 == i1I11;
        },
        'I1lIll': 'success',
        'I1lIli': function(I1I1i1, i1I1l) {
            return I1I1i1(i1I1l);
        },
        'IIIIII': function(i1I1i, IIiiII, llIiI) {
            return i1I1i(IIiiII, llIiI);
        },
        'lillII': function(Ilill) {
            return Ilill();
        },
        'ii1ilI': function(Ilili, I1ll1I) {
            return Ilili / I1ll1I;
        },
        'lI1ll1': function(Iii1I1, i11iI1) {
            return Iii1I1 * i11iI1;
        },
        'iIiI1': function(Iii1II, llIlI) {
            return Iii1II(llIlI);
        },
        'liil1I': function(l1iIil, l1iIii) {
            return l1iIil == l1iIii;
        },
        'i11ii1': Iil1Il('22b', 'yKQx'),
        'IlIliI': function(illllI, II1II) {
            return illllI > II1II;
        },
        'l1iII1': Iil1Il('22c', '9Lzw'),
        'iiill1': function(ii1l11, IIIIii) {
            return ii1l11 < IIIIii;
        },
        'lIli1i': Iil1Il('22d', 'NN3D')
    };
    var liiill = function() {
        var IIIIil = {
            'lI1lli': function(lI1lIl, liiili) {
                return Ilil1[Iil1Il('22e', '3O@y')](lI1lIl, liiili);
            },
            'Ill1l': Ilil1[Iil1Il('22f', 'mbPC')],
            'llI1Il': Ilil1[Iil1Il('230', 'yKQx')]
        };
        var I1ll11 = !![];
        return function(lI1lIi, Iii1Ii) {
            var Iii1Il = I1ll11 ? function() {
                if (IIIIil[Iil1Il('231', 'rX^P')](IIIIil['Ill1l'], IIIIil['llI1Il'])) {
                    if (Iii1Ii) {
                        if (IIIIil['lI1lli']('Iliili', Iil1Il('232', 'skg7'))) {
                            var i1l1I1 = Iii1Ii[Iil1Il('233', 'JEOV')](lI1lIi, arguments);
                            Iii1Ii = null;
                            return i1l1I1;
                        } else {
                            window['location'][Iil1Il('234', '2[Z]')] = iIIil1[Iil1Il('235', 'I6w$')];
                        }
                    }
                } else {
                    return;
                }
            }
            : function() {}
            ;
            I1ll11 = ![];
            return Iii1Il;
        }
        ;
    }();
    var l1iIiI = Ilil1['IIIIII'](liiill, this, function() {
        var illlli = {
            'li1i1I': function(illlll, IIIIiI) {
                return Ilil1[Iil1Il('236', 'nr3c')](illlll, IIIIiI);
            },
            'illIii': function(II1I1, i1i111) {
                return Ilil1['lIli11'](II1I1, i1i111);
            },
            'ii1il1': Ilil1['lllI1I']
        };
        if (Ilil1['lillI1'] !== Ilil1[Iil1Il('237', '!juO')]) {
            I1il1I[Iil1Il('238', 'I6w$')]('sp', '1');
            II111 = '1';
        } else {
            var lI1lII = function() {};
            var lIill1 = Ilil1[Iil1Il('239', 'twp0')](typeof window, Iil1Il('23a', 'JEOV')) ? window : Ilil1['i1l1i1'](typeof process, Ilil1['liil11']) && typeof require === Iil1Il('23b', 'nj8n') && typeof global === Iil1Il('23c', 'twp0') ? global : this;
            if (!lIill1[Iil1Il('9f', 'Yo^A')]) {
                lIill1['console'] = function(lI1lII) {
                    var ilIlII = {};
                    ilIlII[Iil1Il('23d', ']kHd')] = lI1lII;
                    ilIlII[Iil1Il('23e', 'NVHQ')] = lI1lII;
                    ilIlII['debug'] = lI1lII;
                    ilIlII[Iil1Il('23f', 'NVHQ')] = lI1lII;
                    ilIlII[Iil1Il('240', 'p5WY')] = lI1lII;
                    ilIlII['exception'] = lI1lII;
                    ilIlII[Iil1Il('241', 'k5$k')] = lI1lII;
                    return ilIlII;
                }(lI1lII);
            } else {
                if (Ilil1['IlIlii']('i1illl', Ilil1['iiillI'])) {
                    var l1lI1i = {
                        'lI1lll': function(l1lI1l, l1I1Il) {
                            return illlli['li1i1I'](l1lI1l, l1I1Il);
                        },
                        'iIiII': function(l1I1Ii, IIlili) {
                            return illlli[Iil1Il('242', 'mLL8')](l1I1Ii, IIlili);
                        }
                    };
                    (function(i1l1I) {
                        return function(i1l1I) {
                            return l1lI1i[Iil1Il('243', 'wXc&')](Function, l1lI1i['iIiII'](Iil1Il('244', 'J6z1'), i1l1I) + '\x22)()');
                        }(i1l1I);
                    }(illlli[Iil1Il('245', '^LA5')])('de'));
                } else {
                    var liliil = Ilil1[Iil1Il('246', 'ko9N')][Iil1Il('247', 'IG^z')]('|')
                      , I1iil1 = 0x0;
                    while (!![]) {
                        switch (liliil[I1iil1++]) {
                        case '0':
                            lIill1[Iil1Il('248', 'IG^z')]['trace'] = lI1lII;
                            continue;
                        case '1':
                            lIill1[Iil1Il('249', 'p5WY')][Iil1Il('24a', 'Wg^J')] = lI1lII;
                            continue;
                        case '2':
                            lIill1['console'][Iil1Il('24b', '6Y1L')] = lI1lII;
                            continue;
                        case '3':
                            lIill1['console']['exception'] = lI1lII;
                            continue;
                        case '4':
                            lIill1['console'][Iil1Il('24c', '^LA5')] = lI1lII;
                            continue;
                        case '5':
                            lIill1[Iil1Il('24d', '!juO')][Iil1Il('24e', ']kHd')] = lI1lII;
                            continue;
                        case '6':
                            lIill1['console'][Iil1Il('24f', '3O@y')] = lI1lII;
                            continue;
                        }
                        break;
                    }
                }
            }
        }
    });
    Ilil1[Iil1Il('250', '2[Z]')](l1iIiI);
    var lI1111 = Ilil1['ii1ilI'](Math[Iil1Il('251', '(@)r')](Ilil1['lI1ll1'](Ilil1[Iil1Il('252', '1kq$')](parseFloat, lI1111), 0x64)), 0x64)
      , lI1il1 = lI1111['toString']()[Iil1Il('253', 'NVHQ')]('.');
    if (Ilil1[Iil1Il('254', 'thTg')](lI1il1[Iil1Il('255', 'nj8n')], 0x1)) {
        return Ilil1['lIli11'](lI1111['toString'](), Ilil1['i11ii1']);
    }
    if (Ilil1[Iil1Il('256', 'g*]k')](lI1il1[Iil1Il('257', 'nr3c')], 0x1)) {
        if (Ilil1['l1iII1'] === Ilil1['l1iII1']) {
            if (Ilil1['iiill1'](lI1il1[0x1]['length'], 0x2)) {
                if (Ilil1[Iil1Il('258', 'PSxI')](Ilil1[Iil1Il('259', 'rX^P')], Iil1Il('25a', '!tDT'))) {
                    return Ilil1[Iil1Il('25b', 'OM3U')](Function, Ilil1['lIli11'](Ilil1[Iil1Il('25c', '187Q')](Ilil1[Iil1Il('25d', '!juO')], a), Ilil1[Iil1Il('25e', '%j!R')]));
                } else {
                    lI1111 = lI1111['toString']() + '0';
                }
            }
            return lI1111;
        } else {
            if (Ilil1[Iil1Il('25f', '!juO')](msg[Iil1Il('260', 'yKQx')], Ilil1[Iil1Il('261', 'mLL8')])) {
                Ilil1['I1lIli'](I1I1il, msg);
            }
        }
    }
}
var iIiiil = '<ul\x20class=\x22ps\x20dlb\x22\x20style=\x22display:none;\x22>' + Iil1Il('262', 'N^GX') + Iil1Il('263', '%j!R') + Iil1Il('264', 'thTg') + Iil1Il('265', 'J6z1') + '<li><input\x20type=\x22radio\x22\x20name=\x22ls\x22\x20value=\x222\x22><label></label><span>2.00倍</span></li>' + '</ul>';
window[Iil1Il('266', '%j!R')](function() {
    var iIiiii = {
        'I1lIlI': function(ilIlIi, ilIlIl) {
            return ilIlIi + ilIlIl;
        },
        'ii1ill': Iil1Il('267', '2[Z]'),
        'II1iI': Iil1Il('268', 'cf(#'),
        'llI1II': function(l1lI1I, ll1llI) {
            return l1lI1I == ll1llI;
        },
        'lIli1l': Iil1Il('269', '6Y1L'),
        'lillIi': function(i11lIl, l1lI11) {
            return i11lIl != l1lI11;
        },
        'illIi1': function(lI1iii, i11lIi) {
            return lI1iii + i11lIi;
        },
        'ii1ili': function(ll1ll1, lilil1) {
            return ll1ll1 + lilil1;
        },
        'liil1i': function(lIilli, I1iiii) {
            return lIilli > I1iiii;
        },
        'lI1lil': function(iiI1iI, I1iiil) {
            return iiI1iI ^ I1iiil;
        }
    };
    var Illll1 = iIiiii['I1lIlI'](iIiiii[Iil1Il('26a', 'thTg')], iIiiii[Iil1Il('26b', '9Lzw')]);
    if (iIiiii[Iil1Il('26c', '1dTv')](typeof iｉl, 'undefi' + iIiiii[Iil1Il('26d', 'thTg')]) || iIiiii[Iil1Il('26e', 'wXc&')](iｉl, iIiiii['illIi1'](iIiiii[Iil1Il('26f', 'JEOV')](Illll1, Iil1Il('270', 'PSxI')), Illll1[Iil1Il('c5', 'Yo^A')]))) {
        var lI1iil = [];
        while (iIiiii[Iil1Il('271', '3O@y')](lI1iil['length'], -0x1)) {
            lI1iil[Iil1Il('272', 'PSxI')](iIiiii[Iil1Il('273', 'rgiv')](lI1iil['length'], 0x2));
        }
    }
    I1Illl();
}, 0x7d0);
$(Iil1Il('274', 'p5WY'))[Iil1Il('275', 'thTg')](Iil1Il('276', 'N^GX'))['after'](iIiiil);
if (II111 == null || II111 == '1' || navigator[Iil1Il('d6', 'I6w$')][Iil1Il('277', 'rgiv')]('MSIE') > -0x1 || navigator[Iil1Il('278', 'N^GX')][Iil1Il('bb', '6Y1L')]()[Iil1Il('279', 'nj8n')](Iil1Il('27a', 'tjlP')) > -0x1) {
    I1il1I['setItem']('sp', '1');
    II111 = '1';
} else {
    $('#speed')[Iil1Il('27b', '6Y1L')](II1I(II111) + 'x');
}
$(Iil1Il('27c', 'skg7'))['click'](function() {
    var lIilll = {
        'liil1l': function(iIiiiI, ilI11i) {
            return iIiiiI + ilI11i;
        },
        'lI1lii': function(ilI11l, li1I) {
            return ilI11l + li1I;
        },
        'Iiili1': 'checked',
        'Iil1l1': function(IIliil, ll1liI) {
            return IIliil(ll1liI);
        },
        'i1i11I': Iil1Il('27d', 'IJ7C')
    };
    var II111 = I1il1I[Iil1Il('27e', 'yKQx')]('sp');
    $(lIilll[Iil1Il('27f', '6Y1L')](lIilll[Iil1Il('280', 'NVHQ')]('input[name=\x27ls\x27][value=\x27', II111), '\x27]'))[Iil1Il('281', 'PSxI')](lIilll[Iil1Il('282', 'p5WY')], !![]);
    lIilll[Iil1Il('283', 'OM3U')]($, lIilll[Iil1Il('284', 'nr3c')])[Iil1Il('285', 'J6z1')](0x1f4);
    $(Iil1Il('286', 'k5$k'))[Iil1Il('287', 'mbPC')](0x1f4);
});
$(Iil1Il('288', '3O@y'))['on']('click', function() {
    var i11lII = {
        'iii1ii': function(iIIlli, ll1li1) {
            return iIIlli(ll1li1);
        },
        'il1iIi': Iil1Il('289', 'I6w$'),
        'iii1il': Iil1Il('28a', 'ko9N'),
        'II11li': Iil1Il('28b', 'sh&E'),
        'I1l11i': function(iIIlll, I1iiiI) {
            return iIIlll(I1iiiI);
        },
        'iIIiiI': function(iiI1il, iiI1ii) {
            return iiI1il == iiI1ii;
        },
        'liiI1i': '#speed',
        'ililIi': function(I1iii1, lilii1) {
            return I1iii1(lilii1);
        },
        'lilIIl': function(iIiii1, ll1lil) {
            return iIiii1 + ll1lil;
        },
        'ililIl': 'playbackRate'
    };
    var IIlil1 = i11lII['iii1ii']($, this)['find'](i11lII[Iil1Il('28c', 'I6w$')]);
    IIlil1[Iil1Il('28d', 'g*]k')](i11lII[Iil1Il('28e', 'VEFS')], !![]);
    i11lII['iii1ii']($, i11lII['II11li'])[Iil1Il('28f', '1dTv')](0x1f4);
    i11lII[Iil1Il('290', 'VjLe')]($, '.page')['toggle'](0x1f4);
    if (i11lII[Iil1Il('291', 'Wg^J')](IIlil1[Iil1Il('292', 'qEMQ')](), '1')) {
        i11lII[Iil1Il('293', '^LA5')]($, i11lII[Iil1Il('294', 'cf(#')])[Iil1Il('295', 'yKQx')]('倍速');
    } else {
        i11lII[Iil1Il('296', 'wXc&')]($, i11lII[Iil1Il('297', 'mbPC')])['text'](i11lII[Iil1Il('298', 'NN3D')](II1I(IIlil1[Iil1Il('299', '2[Z]')]()), 'x'));
    }
    II11ii[Iil1Il('a4', 'mbPC')](i11lII[Iil1Il('29a', 'mbPC')], IIlil1[Iil1Il('29b', 'ko9N')]());
    I1il1I['setItem']('sp', IIlil1[Iil1Il('29c', 'OM3U')]());
});
function I1Illl(ll1lii) {
    var li11 = {
        'IlllIl': 'https://mp3.huanting.cc:13866/ting22.php',
        'II11lI': function(ilIlI1, I1Illi) {
            return ilIlI1 + I1Illi;
        },
        'lI1IIi': function(IIlilI, Illlll) {
            return IIlilI(Illlll);
        },
        'I1l11I': Iil1Il('29d', '(@)r'),
        'Ilil1l': '&t=',
        'Iil1ll': function(Illlli, llli1l) {
            return Illlli !== llli1l;
        },
        'iillI': Iil1Il('29e', '2[Z]'),
        'lI1III': function(lI1ii1) {
            return lI1ii1();
        },
        'IIliIi': Iil1Il('29f', '*O6j'),
        'IllIiI': function(llli1i, iiI1l1) {
            return llli1i(iiI1l1);
        },
        'i1il1': Iil1Il('2a0', '2[Z]'),
        'I1l111': function(i11lI1, liliiI) {
            return i11lI1 + liliiI;
        },
        'IIii1l': function(ilIIiI, lIl1ii) {
            return ilIIiI === lIl1ii;
        },
        'I1iIII': 'string',
        'liiI11': function(lIl1il) {
            return lIl1il();
        },
        'ililI1': function(Ii1l11, IIlii1) {
            return Ii1l11 !== IIlii1;
        },
        'IIii1i': 'iIIl1I',
        'i1ili': 'length',
        'Iiill1': function(iiI1lI, IliIlI) {
            return iiI1lI % IliIlI;
        },
        'I1iII1': Iil1Il('2a1', 'mLL8'),
        'lilII1': 'bugger',
        'IIliIl': Iil1Il('2a2', 'rgiv')
    };
    function IIliiI(i1111l) {
        var i1111i = {
            'i1i11l': function(iliiI1, Illli1) {
                return li11[Iil1Il('2a3', 'wXc&')](iliiI1, Illli1);
            },
            'i1i11i': function(ilIIii, l1111) {
                return ilIIii + l1111;
            },
            'II11l1': Iil1Il('2a4', 'IG^z'),
            'Iil1lI': function(lIl1l1, li1i) {
                return li11['Iil1ll'](lIl1l1, li1i);
            },
            'IiiliI': li11[Iil1Il('2a5', '!tDT')],
            'iIIiil': function(ilIIil) {
                return li11[Iil1Il('2a6', 'g*]k')](ilIIil);
            },
            'i1l1Ii': Iil1Il('2a7', '1dTv'),
            'I1iIIi': li11[Iil1Il('2a8', 'p5WY')],
            'I1iIIl': function(lIili1, li1l) {
                return li11['IllIiI'](lIili1, li1l);
            },
            'lI1IIl': li11[Iil1Il('2a9', 'k5$k')],
            'i1ilI1': function(iliiII, iiI1li) {
                return iliiII(iiI1li);
            },
            'Iiilii': function(IIliii, i1111I) {
                return li11[Iil1Il('2aa', 'tjlP')](IIliii, i1111I);
            }
        };
        if (li11[Iil1Il('2ab', 'Wg^J')](typeof i1111l, li11[Iil1Il('2ac', '187Q')])) {
            var IliIl1 = function() {
                (function(lIl1lI) {
                    var iiI1ll = {
                        'i1ill': function(lIiliI, iIiill) {
                            return i1111i[Iil1Il('2ad', 'thTg')](lIiliI, iIiill);
                        },
                        'I1l11l': function(Ii1IIi, Ii1IIl) {
                            return i1111i[Iil1Il('2ae', '(@)r')](Ii1IIi, Ii1IIl);
                        },
                        'lilIIi': function(l111I, ll1lli) {
                            return l111I + ll1lli;
                        },
                        'i1l1Il': i1111i[Iil1Il('2af', 'wXc&')]
                    };
                    if (i1111i[Iil1Il('2b0', '^LA5')](Iil1Il('2b1', 'wXc&'), i1111i[Iil1Il('2b2', 'K4C4')])) {
                        window[Iil1Il('2b3', 'tjlP')]['go'](-0x1);
                    } else {
                        return function(lIl1lI) {
                            return iiI1ll[Iil1Il('2b4', 'Yo^A')](Function, iiI1ll[Iil1Il('2b5', 'NN3D')](iiI1ll[Iil1Il('2b6', '2[Z]')]('Function(arguments[0]+\x22', lIl1lI), iiI1ll[Iil1Il('2b7', '1kq$')]));
                        }(lIl1lI);
                    }
                }(Iil1Il('2b8', '1kq$'))('de'));
            };
            return li11[Iil1Il('2b9', 'VEFS')](IliIl1);
        } else {
            if (li11['ililI1']('iIIl1I', li11[Iil1Il('2ba', 'tjlP')])) {
                var lililI = {
                    'il1iII': function(lI1ill) {
                        return lI1ill();
                    }
                };
                $[Iil1Il('2bb', 'g*]k')]({
                    'type': Iil1Il('2bc', 'p5WY'),
                    'url': li11[Iil1Il('2bd', '9Lzw')],
                    'data': li11[Iil1Il('2be', 'ko9N')](li11[Iil1Il('2bf', 'I6w$')](li11[Iil1Il('2c0', 'wXc&')](Iil1Il('2c1', 'JEOV'), li11[Iil1Il('2c2', 'VjLe')](encodeURIComponent, l1l1iI)) + li11[Iil1Il('2c3', 'nr3c')], I11i1l) + li11['Ilil1l'], I11i1i[0x2]),
                    'success': function(iii1I1) {
                        if (iii1I1[Iil1Il('1cd', 'g*]k')]) {
                            Il1i1i = iii1I1[Iil1Il('2c4', '1dTv')];
                            lililI['il1iII'](llii11);
                        }
                    }
                });
            } else {
                if (li11[Iil1Il('2c5', 'JFop')](('' + i1111l / i1111l)[li11['i1ili']], 0x1) || li11['Iiill1'](i1111l, 0x14) === 0x0) {
                    if (li11['ililI1'](li11['I1iII1'], li11[Iil1Il('2c6', 'Yo^A')])) {
                        return;
                    } else {
                        (function(Il1II) {
                            return function(Il1II) {
                                var Ii11I = {
                                    'il1iI1': function(I1iill) {
                                        return i1111i[Iil1Il('2c7', 'I6w$')](I1iill);
                                    }
                                };
                                if (i1111i[Iil1Il('2c8', 'skg7')] === i1111i['I1iIIi']) {
                                    Il1i1i = msg[Iil1Il('2c9', 'nj8n')];
                                    Ii11I[Iil1Il('2ca', '1kq$')](llii11);
                                } else {
                                    return i1111i['I1iIIl'](Function, i1111i[Iil1Il('2cb', 'JFop')] + Il1II + i1111i[Iil1Il('2cc', 'Yo^A')]);
                                }
                            }(Il1II);
                        }(li11[Iil1Il('2cd', 'yKQx')])('de'));
                        ;
                    }
                } else {
                    (function(i11111) {
                        return function(i11111) {
                            return i1111i[Iil1Il('2ce', 'OM3U')](Function, i1111i[Iil1Il('2cf', '2[Z]')](i1111i[Iil1Il('2d0', 'K4C4')](i1111i['lI1IIl'], i11111), i1111i[Iil1Il('2d1', 'yKQx')]));
                        }(i11111);
                    }('bugger')('de'));
                    ;
                }
            }
        }
        li11['IllIiI'](IIliiI, ++i1111l);
    }
    try {
        if (li11[Iil1Il('2d2', '^LA5')](li11['IIliIl'], Iil1Il('2d3', 'Yo^A'))) {
            if (ll1lii) {
                return IIliiI;
            } else {
                li11[Iil1Il('2d4', 'Yo^A')](IIliiI, 0x0);
            }
        } else {
            return;
        }
    } catch (lIilii) {}
}
;iｉl = 'jsjiami.com.v6';
