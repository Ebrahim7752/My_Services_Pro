$(document).ready(function () {

    "use strict";

    /* ================= PRELOADER ================= */
    $(window).on("load", function () {
        $('.preloader-holder .loading').fadeOut();
        $('.preloader-holder').delay(350).fadeOut('slow');
        $('body').delay(350).css({'overflow': 'visible'});
    });

    /* ================= FIXED NAVBAR ================= */
    $(window).on("scroll", function () {
        if ($(window).scrollTop() > 34) {
            $(".navbar").addClass("navbar-light");
        } else {
            $(".navbar").removeClass("navbar-light");
        }
    });

    /* ================= TESTIMONIALS ================= */
  $("#owl-testimonials").owlCarousel({
    items: 1,                    // عرض عنصر واحد فقط
    loop: true,                   // تكرار اللوب
    margin: 10,                   // مسافة بين العناصر (اختياري)
    nav: true,                    // أسهم التنقل
    navText: ["<i class='bx bx-left-arrow-alt'></i>", "<i class='bx bx-right-arrow-alt'></i>"],
    dots: true,                   // النقاط أسفل الكاروسيل
    autoplay: true,               // تشغيل تلقائي
    autoplayTimeout: 6000,        // الانتقال كل 6 ثواني
    autoplayHoverPause: true,     // التوقف عند مرور الماوس
    animateOut: "fadeOut",        // تأثير الخروج
    animateIn: "fadeIn",          // تأثير الدخول
    smartSpeed: 500
});

    /* ================= SCREENSHOTS ================= */
    $("#owl-screenshots").owlCarousel({
        autoPlay: 3000,
        items: 3,
        itemsDesktop: [1199, 3],
        itemsDesktopSmall: [979, 2],
        itemsTablet: [768, 1],
        itemsMobile: [479, 1]
    });

    /* ================= BRANDS ================= */
    $("#owl-brands").owlCarousel({
        autoPlay: 3000,
        items: 4,
        itemsDesktop: [1199, 4],
        itemsDesktopSmall: [979, 3],
        itemsTablet: [768, 2],
        itemsMobile: [479, 1]
    });

    /* ================= OTHER APPS (المهم) ================= */
    $("#other-apps .owl-carousel").owlCarousel({
        autoPlay: 3000,
        stopOnHover: true,
        items: 3,
        itemsDesktop: [1199, 3],
        itemsDesktopSmall: [979, 2],
        itemsTablet: [768, 1],
        itemsMobile: [479, 1],
        navigation: true,
        pagination: false
    });

    /* ================= WOW ================= */
    new WOW().init();

});













$(document).ready(function(){
    // لجميع الروابط الداخلية التي تبدأ بـ #
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault(); // منع السلوك الافتراضي
        var target = this.hash;
        var $target = $(target);

        // النزول بسلاسة
        $('html, body').animate({
            scrollTop: $target.offset().top
        }, 800); // 800 ملي ثانية للنزول
    });
});
