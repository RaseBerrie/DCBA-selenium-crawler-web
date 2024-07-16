/*************** CONSTANTS ***************/
const DROPTWO = `<li class="dropdown-item">
                <a class="link-secondary link-underline-opacity-0" href="#" style="pointer-events: none;">
                    회사명을 먼저 선택하세요.
                </a></li>`
const DROPTHREE = `<li class="dropdown-item">
                <a class="link-secondary link-underline-opacity-0" href="#" style="pointer-events: none;">
                    루트 도메인을 먼저 선택하세요.
                </a></li>`

/*************** DEFAULT ***************/
function menuClick() {
    $('#side-nav-list li').on('click', function() {
        var activeTab = $(this).attr("id");
        location.href = '/' + activeTab;
    }
)} 

function scrollTop() {
    if ($(window).scrollTop() > 500) {
        $(".backToTopBtn").addClass("active");
    } else {
        $(".backToTopBtn").removeClass("active");
    }}
    $(function() {
        scrollTop();
        $(window).on("scroll", scrollTop);

    $(".backToTopBtn").click(function () {
        $("html, body").animate({ scrollTop: 0 }, 1);
        return false;
    });
});

function foldableButton() {
    $('.see-more').click(function() {
        $(this).parent('.show-less').hide();
        $(this).parent('.show-less').siblings('.show-more').show();
    });

    $('.see-less').click(function() {
        $(this).parent('.show-more').hide();
        $(this).parent('.show-more').siblings('.show-less').show();
    });
}

function downloadButton(pagename) {
    $('#download').on('click', function(event) {
        event.preventDefault();
        var isTagActive = false;

        if($(".top-align-box").find(".active").text()) isTagActive = true
        if (!queryed && !isTagActive) {
            downloadUrl = pagename + '/default?filedownload=true'
        } else {
            const menu = $('#search-param').val();
            const query = $('#searchInput').val();

            if(isTagActive) {
                tag = $(".top-align-box").find(".active").text();
                if(tag === "기타") tag = "others";
            } else tag = ''

            if(pagename === "/fileparses") {
                switch(menu) {
                    case "파일 이름": param = 'title'; break;
                    case "주요 데이터": param = 'parsed_data'; break;
                    default: param = '';
                }
            } else {
                switch(menu) {
                    case "서브도메인": param = 'subdomain'; break;
                    case "제목": param = 'title'; break;
                    case "URL": param = 'url'; break;
                    case "콘텐츠": param = 'content'; break;
                    default: param = '';
                }
            }
            downloadUrl = pagename + '/result?tag=' + tag + '&menu=' + param + '&key=' + query + '&filedownload=true'
        }
        window.location.href = downloadUrl;
    });
}

/*************** MENU CONTROL ***************/
function sideMenu() {
    $('.summary').click(function() {
        var sideOptions = $(this).siblings('.side-options');
        var icon = $(this).find('.fa-solid');
        
        sideOptions.toggle();
        if (sideOptions.is(':visible')) {
            icon.removeClass('fa-circle-chevron-right');
            icon.addClass('fa-circle-chevron-down');
        } else {
            icon.removeClass('fa-circle-chevron-down');
            icon.addClass('fa-circle-chevron-right');
        }
    })
}

function topMenu() {
    $('.nav-tabs #drop-btn-1').find('a').click(function(e) {
        e.preventDefault();
        var concept = $(this).text().replace(/\n/g, "").replace(/\s*/g, "");
        var id = $(this).attr('value');
        $('#drop-1').text(concept);

        $('#drop-2').text("루트 도메인");
        $('#second-level-menu').html(DROPTWO);

        $('#drop-3').text("서브 도메인");
        $('#third-level-menu').html(DROPTHREE);

        var cookie = {"comp": [Number(id), concept], "root": [0, "루트 도메인"], "sub": [0, "서브 도메인"]};
        $.cookie("topMenu", JSON.stringify(cookie));

        $(".selected").trigger("click");
    });

    $('.nav-tabs #drop-btn-2').find('a').click(function(e) {
        e.preventDefault();
        var concept = $(this).text().replace(/\n/g, "").replace(/\s*/g, "");
        var id = $(this).attr('value');
        $('#drop-2').text(concept);
        
        $('#drop-3').text("서브 도메인");
        $('#third-level-menu').html(DROPTHREE);

        var cookie = JSON.parse($.cookie("topMenu"));
        cookie.root = [Number(id), concept]; cookie.sub = [0, "서브 도메인"];
        $.cookie("topMenu", JSON.stringify(cookie));

        $(".selected").trigger("click");
    });

    $('.nav-tabs #drop-btn-3').find('a').click(function(e) {
        e.preventDefault();
        var concept = $(this).text().replace(/\n/g, "").replace(/\s*/g, "");
        var id = $(this).attr('value');

        $('#drop-3').text(concept);
        var cookie = JSON.parse($.cookie("topMenu")); cookie.sub = [Number(id), concept];
        $.cookie("topMenu", JSON.stringify(cookie));

        $(".selected").trigger("click");
    });
}

function searchMenu() {
    $('.input-group').find('a').click(function(e) {
        e.preventDefault();
        var concept = $(this).text();
        $('#search-concept').text(concept);
        $('#search-param').val(concept);
    });
}

/*************** OUTPUT ***************/
function loadDashBoard() {
    var resultlabel = []
    var resultcount = []

    $.get('dashboard/default', function(data) {
        data.forEach(data => {
            resultlabel.push(data[0]);
            resultcount.push(data[1]);
        });
        new Chart(document.getElementById("bar-chart"), {
            type: 'bar',
            data: {
            labels: resultlabel,
            datasets: [
                { data: resultcount }
            ]
            },
            options: {
            legend: { display: false },
            title: { display: true, text: "크롤링 데이터 개수" },
            }
        });
    });
}

function loadInitiateResults(reset, pagename) {
    if (loading) return;
    
    loading = true;
    $('#loading').show();

    let tag = '';
    if(pagename === "/fileparses") {
        if($(".top-align-box").find(".active").text() != undefined) {
            tag = $(".top-align-box").find(".active").text();
            if(tag === "기타") tag = "others";
        }
    }

    $.get(pagename + '/default', { tag: tag, page: page }, function(data) {
        if (reset) endofdata = false;

        $('#results').append(data);
        $('#loading').hide();

        var count = $('#count-result').text();
        $('.top-total strong').text(count);

        searchMenu(); foldableButton();
        loading = false; page++;
    });
}

function loadResults(reset, pagename) {
    if (loading) return;

    loading = true;
    $('#loading').show();

    const menu = $('#search-param').val();
    const query = $('#searchInput').val();
    
    let tag = '';
    let param;

    /* 파일 식별 */
    if(pagename === "/fileparses") {
        switch(menu) {
            case "파일 이름": param = 'title'; break;
            case "주요 데이터": param = 'parsed_data'; break;
            default: param = '';
        }
        if($(".top-align-box").find(".active").text() != undefined) {
            tag = $(".top-align-box").find(".active").text();
            if(tag === "기타") tag = "others";
        }
    } else {
        switch(menu) {
            case "서브도메인": param = 'subdomain'; break;
            case "제목": param = 'title'; break;
            case "URL": param = 'url'; break;
            case "콘텐츠": param = 'content'; break;
            default: param = '';
        }
    }

    if (query) {
        $.get(pagename + "/result", { tag: tag, menu: param, key: query, page: page }, function(data) {
            if (reset) endofdata = false;

            $('#results').append(data);
            $('#loading').hide();

            var count = $('#count-result').text();
            $('.top-total strong').text(count);

            searchMenu(); foldableButton();
            loading = false; page++;
        });
    }
}
