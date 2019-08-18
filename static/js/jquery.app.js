/**
 * Theme: Minton Admin Template
 * Author: Coderthemes
 * Module/App: Main Js
 */


(function ($) {

    'use strict';

    function initNavbar() {
        $('.navbar-toggle').on('click', function (event) {
            $(this).toggleClass('open');
            $('#navigation').slideToggle(400);
        });

        //$('.navigation-menu>li').slice(-1).addClass('last-elements');

        $('.navigation-menu li.has-submenu a[href="#"]').on('click', function (e) {
            if ($(window).width() < 992) {
                e.preventDefault();
                $(this).parent('li').toggleClass('open').find('.submenu:first').toggleClass('open');
            }
        });
    }

    function initToast() {
        function toast(msg, type) {
            $.bootstrapGrowl(msg, {
                ele: "body", // which element to append to
                type: type, // (null, 'info', 'danger', 'success')
                offset: {from: "top", amount: 20}, // 'top', or 'bottom'
                align: "right", // ('left', 'right', or 'center')
                width: 500, // (integer, or 'auto')
                delay: 5000, // Time while the message will be displayed. It's not equivalent to the *demo* timeOut!
                allow_dismiss: true, // If true then will display a cross to close the popup.
                stackup_spacing: 10 // spacing between consecutively stacked growls.
            });
        }

        window.showError = function (msg) {
            toast(msg, "danger");
        };

        window.showInfo = function (msg) {
            toast(msg, "info");
        };

        window.showSuccess = function (msg) {
            toast(msg, "success");
        };

        window.coming = function () {
            showInfo("Coming soon!");
        };
    }

    function initScroll2Top() {
        $(window).scroll(function () {
            ( $(this).scrollTop() > 300 ) ? $("a#scroll-to-top").addClass('visible') : $("a#scroll-to-top").removeClass('visible');
        });

        $("a#scroll-to-top").click(function () {
            $("html, body").animate({scrollTop: 0}, "slow");
            return false;
        });
    }


    function init() {
        initNavbar();
        initToast();
        initScroll2Top()
    }

    init();

})(jQuery)

