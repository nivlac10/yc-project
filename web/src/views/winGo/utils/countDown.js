(function () {
    function Timer(delay, callback) {
        this._delay = delay;
        this._callback = callback;
        this._interval = setInterval(callback, delay);
    }

    function Countdown(config) {
        var defaultOptions = {
            fixNow: 3 * 1000,
            fixNowDate: true,
            now: Date.now(),
            template: '{d}:{h}:{m}:{s}',
            render: function (outstring) {
                console.log(outstring);
            },
            end: function () {
                console.log('结束！');
            },
            endTime: Date.now() + 5 * 1000 * 60
        };

        Object.assign(this, defaultOptions, config);
        this.init();
    }

    Countdown.prototype = {
        constructor: Countdown,
        init: function () {
            if (this.fixNowDate) {
                var self = this;
                var fixTimer = new Timer(this.fixNow, function () {
                    self.getNowTime(function (now) {
                        console.log('服务器时间校准,' + self.now + '----------' + now);
                        self.now = now;
                    });
                });
            }

            var msInterval = new Timer(this._delay, () => {
                this.now += this._delay;
                if (this.now >= this.endTime) {
                    msInterval.clearInterval();
                    this.end();
                } else {
                    this.render(this.getOutString());
                }
            });
        },
        getBetween: function () {
            return this._formatTime(this.endTime - this.now);
        },
        getOutString: function () {
            var between = this.getBetween();
            return this.template.replace(/{(\w*)}/g, (match, key) => between.hasOwnProperty(key) ? between[key] : "");
        },
        getNowTime: function (cb) {
            var xhr = new XMLHttpRequest();
            xhr.open('get', '/', true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 3) {
                    var now = xhr.getResponseHeader('Date');
                    cb(new Date(now).valueOf());
                }
            };
            xhr.send(null);
        },
        _cover: function (num) {
            var n = parseInt(num, 10);
            return n < 10 ? '0' + n : n;
        },
        _formatTime: function (ms) {
            var s = ms / 1000,
                m = s / 60;
            return {
                d: this._cover(m / 60 / 24),
                h: this._cover(m / 60 % 24),
                m: this._cover(m % 60),
                s: this._cover(s % 60)
            };
        }
    };

    window.$countDown = Countdown;

})();
