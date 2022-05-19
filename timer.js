// import moment from './js/moment.min'

window.onload = function () {
    timer = (target, date, expected, gmt_offset) => {
        var target_ = target
        var gmt_offset = gmt_offset
        if (gmt_offset >= 0) {
            gmt_offset = "+" + gmt_offset.toString()
        }
        else {
            gmt_offset = "-" + gmt_offset.toString()
        }
        var target = document.querySelector(target);
        // var countDownDate = new Date(date).getTime(); // it is written in Pacific time
        var deadline_time = moment.tz(date, "Etc/GMT" + gmt_offset).format('ddd MMM DD YYYY HH:mm:ss [GMT]ZZ') // Deadline in timezone from conference website.
        // Thu 2022-05-19 13:00 GMT-0700 
        // Tue Nov 16 2021 23:59:59 GMT-0800
        var deadline_local_time = moment(date).local().format('ddd MMM DD YYYY HH:mm:ss [GMT]ZZ') // Deadline in local timezone.
        var local_name = moment.tz.guess()

        //console.log(target_, deadline_time)
        //console.log(target_, deadline_local_time)

        setInterval(() => {
            //var now = new Date().getTime();
            //var currentDate = moment().local();
            //var currentDatevalue = currentDate.valueOf()
            //var currentPSTDate = moment.tz(now, "America/Los_Angeles");
            //var currentPSTDatevalue = currentPSTDate.valueOf()
            // var distance = countDownDate - now;
            // var distance = countDownDate - currentPSTDatevalue;

            var end = moment.tz(date, "Etc/GMT" + gmt_offset).valueOf()
            var start = moment().local().valueOf()
            // alert("SSS " + end + "D  " + start)
            var distance = end - start;


            var days = Math.floor(distance / (1000 * 60 * 60 * 24)).toLocaleString('en-US', { minimumIntegerDigits: 2 });
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)).toLocaleString('en-US', { minimumIntegerDigits: 2 });
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)).toLocaleString('en-US', { minimumIntegerDigits: 2 });
            var seconds = Math.floor((distance % (1000 * 60)) / 1000).toLocaleString('en-US', { minimumIntegerDigits: 2 });

            // target.innerText =
            //     days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
            if (expected == 1) {
                target.innerHTML = target.innerHTML = "<timeleft>" + days + "d " + hours + "h " + minutes + "m " + seconds + "s " + "</timeleft> <deadline>(Expected)</deadline>" + "<br/><deadline>Deadline in timezone from conference website : " + deadline_time + " </deadline> <br/> <deadline>Deadline in your local " + local_name + " timezone : " + deadline_local_time + " </deadline>";
            }
            else {
                target.innerHTML = target.innerHTML = "<timeleft>" + days + "d " + hours + "h " + minutes + "m " + seconds + "s " + "</timeleft>" + "<br/><deadline>Deadline in timezone from conference website : " + deadline_time + " </deadline> <br/> <deadline>Deadline in your local " + local_name + " timezone : " + deadline_local_time + " </deadline>";
            }

            if (distance < 0) {
                target.innerHTML = "<timeleft>Expired</timeleft>" + "<br/><deadline>Deadline in timezone from conference website : " + deadline_time + " </deadline> <br/> <deadline>Deadline in your local " + local_name + " timezone : " + deadline_local_time + " </deadline>";
            }
        }, 1000);
    };

    timer("#neurips2022timer", "May 19, 2022 20:00:00", 0, +7); // UTC
    timer("#sfn2022timer", "Jun 15, 2022 17:00:00", 0, +4); // EDT
    timer("#opt2022timer", "Sep 17, 2022 20:00:00", 1, +7); // UTC
    timer("#aaai2023timer", "Aug 30, 2022 23:59:59", 1, +7);
    timer("#isbi2023timer", "Oct 15, 2022 23:59:59", 1, +8);
    timer("#cvpr2023timer", "Nov 18, 2022 11:59:59", 1, +8);
    timer("#embc2023timer", "Jan 31, 2023 12:59:59", 1, +8);
    timer("#miccai2023timer", "Mar 1, 2023 23:59:59", 1, +8); // Pacific
    timer("#sfn2023timer", "Jun 15, 2023 17:00:00", 1, +4); // EDT
    //timer("#timer2", "Jan 5, 2022 21:37:49");
    //timer("#timer3", "Jan 5, 2024 22:45:15");
}