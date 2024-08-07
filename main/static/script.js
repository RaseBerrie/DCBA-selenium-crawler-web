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

function resizeWindow() {
	if ($(window).width() < 991) {
		$('.sidebar-wrapper').addClass('collapse').removeClass('show');
		$('.btn-close').show()
	} else {
		$('.sidebar-wrapper').addClass('show').removeClass('collapse');
		$('.btn-close').hide()
	}	
}

function pageClick() {
    $('.pagination .page-item').on('click', function() {
        var clickedPage = $(this).find('.page-link').text();
        clickedPage = String(clickedPage).replace(/^\s+|\s+$/g, '');

        if (clickedPage == "이전") page = parseInt(page) - 1;
        else if (clickedPage == "다음") page = parseInt(page) + 1;
        else if (clickedPage == "처음") page = 1;
        else if (clickedPage == "마지막") {
            if (page % 15 != 0) {
                page = parseInt( $('#count-result').text() / 15 ) + 1;
            } else page = parseInt( $('#count-result').text() / 15 );
        }
        else page = clickedPage;

        if (queryed) loadResults(true, pagename);
        else loadInitiateResults(true, pagename);
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
    $('.show-less').each(function() {
        if ($(this).find('.length').width() > $(this).parent('td').width()) {
            $(this).find('.text-truncate').show();
            
            $(this).siblings('.show-more').hide();
            $(this).find('.length').hide();
        } else {
            $(this).find('.text-truncate').hide();

            $(this).siblings('.show-more').remove();
            $(this).find('.see-more').remove();
        }
    });

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
                switch(tag) {
                    case "기타": tag = "others"; break;
                    case "에러 페이지": tag = "error"; break;
                    case "샘플 페이지": tag = "sample"; break;
                    case "서버 정보 노출": tag = "servinfo"; break;
                }
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

        var cookie = JSON.parse($.cookie("topMenu"));
        cookie.comp = [Number(id), concept]; cookie.root = [0, "루트 도메인"]; cookie.sub = [0, "서브 도메인"];
        $.cookie("topMenu", JSON.stringify(cookie));

        if (queryed) {
            page = 1;
            loadResults(true, pagename);
        }
        else {
            page = 1;
            loadInitiateResults(true, pagename);
        }
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

        if (queryed) {
            page = 1;
            loadResults(true, pagename);
        }
        else {
            page = 1;
            loadInitiateResults(true, pagename);
        }
    });

    $('.nav-tabs #drop-btn-3').find('a').click(function(e) {
        e.preventDefault();
        var concept = $(this).text().replace(/\n/g, "").replace(/\s*/g, "");
        var id = $(this).attr('value');

        $('#drop-3').text(concept);
        var cookie = JSON.parse($.cookie("topMenu")); cookie.sub = [Number(id), concept];
        $.cookie("topMenu", JSON.stringify(cookie));

        loadInitiateResults(true, pagename);
    });
}

function loadContent() {
    if(pagename.substr(1) != 'neednot' && pagename != '/fileparses') $('.btn-group').hide();
    $('#' + pagename.substr(1)).addClass("selected");

    var cookie = JSON.parse($.cookie('status'));
    $('input:checkbox[id="filter"]').prop('checked', cookie.filter);

    $('input:checkbox[id="filter"]').on('click', function() {
        cookie.filter = !cookie.filter;
        $.cookie("status", JSON.stringify(cookie));        
        $('input:checkbox[id="filter"]').prop('checked', cookie.filter);

        if (queryed) {
            page = 1;
            loadResults(true, pagename);
        }
        else {
            page = 1;
            loadInitiateResults(true, pagename);
        }
    });

    $('#searchForm').on('submit', function(event) {
        event.preventDefault();
        $('#results').empty();

        page = 1;
        queryed = true;
        loadResults(true, pagename);
    });

    $('.tags').on('click', function(event) {
        event.preventDefault();
        $('#results').empty();

        $(this).addClass('active').siblings().removeClass('active');

        if (queryed) {
            page = 1;
            loadResults(true, pagename);
        }
        else {
            page = 1;
            loadInitiateResults(true, pagename);
        }
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

function pagingButtons() {
    var count = $('#count-result').text();
    if (count == 0) count = 1;

    let countResult = $('#count-result').text();
    let countPages = Math.ceil(countResult / 15);

    HTML = ''
    if (page != 1) { 
        HTML = `
        <li class="page-item">
        <a class="page-link" href="#" aria-label="Previous">
            <span style="display: none;">처음</span>
            <i class="fa-solid fa-angles-left"></i>
        </a></li>
        <li class="page-item">
        <a class="page-link" href="#" aria-label="Previous">
            <span aria-hidden="true">이전</span>
        </a></li>`
    }

    if (countPages > 10) {
        pageInt = parseInt(page);
        if (pageInt > 5) {
            let end = pageInt + 5
            if (end > countPages) end = countPages + 1;

            let i = end - 10
            if (i < 0) i = 1

            for (i; i < end; i++) {
                HTML += '<li class="page-item" id="page-'
                HTML += i;
                HTML += '"><a class="page-link" href="#">';
                HTML += i;
                HTML += '</a></li>'; }
        } else {
            for (let i = 1; i < 10; i++) {
                HTML += '<li class="page-item" id="page-'
                HTML += i;
                HTML += '"><a class="page-link" href="#">';
                HTML += i;
                HTML += '</a></li>'; }}
        
    } else {
        for (let i = 0; i < countPages; i++) {
            HTML += '<li class="page-item" id="page-'
            HTML += i + 1;
            HTML += '"><a class="page-link" href="#">';
            HTML += i + 1;
            HTML += '</a></li>'; }
    }

    if(page < countPages) {
        HTML += `<li class="page-item">
                <a class="page-link" href="#" aria-label="Next">
                    <span aria-hidden="true">다음</span>
                </a></li>
                <li class="page-item">
                <a class="page-link" href="#" aria-label="Next">
                    <span style="display: none;">마지막</span>
                    <i class="fa-solid fa-angles-right"></i>
                </a></li>`
            }

    $('#page-number').empty()
    $('#page-number').append(HTML);
    pageClick();
}

/*************** OUTPUT ***************/
function loadDashBoard() {
    let compTitle = []
    let dataCount = {
        'total': [],
        'dist': {
            'page': [],
            'file': [],
            'expose': []
        }};

    $.get('dashboard/default', function(data) {
        console.log(data);
        data.slice(1).forEach(row => {
            let tagSum = row[2];
            row.slice(3).forEach(
                function(value, index) { row[index + 3] = value / tagSum }
            );

            compTitle.push(row[0].slice(0,4));
            dataCount.total.push(row[1]);

            dataCount.dist.page.push(row[3] + row[4])
            dataCount.dist.file.push(row[5])
            dataCount.dist.expose.push(row[6] + row[7])
        });

        let keyTotal = data[0][0]
        let bingDone = data[0][1]
        let googleDone = data[0][2]

        let percentLabelOption = {
            formatter: function(value, _context) {
                return Math.round(value * 100) + '%';
                },
            color: '#FFFFFF',
            backgroundColor: 'rgba(0, 0, 0, .5)',
            borderRadius: '4',
        }

        let numberLabelOption = {
            formatter: function(value, _context) {
                return value + '건';
            },
            align: 'end',
            color: '#FFFFFF',
            backgroundColor: 'rgba(0, 0, 0, .5)',
            borderRadius: '4',
        }

        new Chart(document.getElementById("distribution-chart"), {
            plugins: [ChartDataLabels],
            type: 'bar',
            data: {
                labels: compTitle,
                datasets: [{
                    label: '관리자/로그인 페이지',
                    data: dataCount.dist.page,
                    borderWidth: 1,
                    datalabels: percentLabelOption
                },
                {
                    label: '파일 다운로드',
                    data: dataCount.dist.file,
                    borderWidth: 1,
                    datalabels: percentLabelOption
                },
                {
                    label: '정보 노출 페이지',
                    data: dataCount.dist.expose,
                    borderWidth: 1,
                    datalabels: percentLabelOption
                }]
            },
            options: {
                indexAxis: 'y',
                scales: {
                    x: {
                        stacked: true,
                        ticks: {
                            callback: function(value, _index, _values) {
                                return value * 100;
                            }
                        },
                        max: 1
                    },
                    y: { stacked: true }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                },
            }
        });

        new Chart(document.getElementById("totalcount-chart"), {
            plugins: [ChartDataLabels],
            type: 'bar',
            data: {
                labels: compTitle,
                datasets: [
                    {
                        data: dataCount.total,
                        borderWidth: 1,
                        datalabels: numberLabelOption
                    }
                ]
            },
            options: {
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        type: 'logarithmic',
                        ticks: {
                            callback: function(value, _index, _values) {
                                const remain = value / (Math.pow(10, Math.floor(Math.log10(value))));
                                if (remain === 1) {
                                    return value;
                                }
                                return null;
                            }           
                        }
                    }
                }
            }
        });

        new Chart(document.getElementById("google-progress"), {
            plugins: [ChartDataLabels],
            type: 'doughnut',
            data: {
                labels: ['완료', '미완료'],
                datasets: [
                    {
                        data: [googleDone/keyTotal, (keyTotal-googleDone)/keyTotal],
                        datalabels: percentLabelOption
                    }
                ]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Google 검색 진행 상황',
                        font: { family: 'Pretendard', size: 14 },
                    },
                    legend: { position: 'bottom' }
                },
            }
        });

        new Chart(document.getElementById("bing-progress"), {
            plugins: [ChartDataLabels],
            type: 'doughnut',
            data: {
                labels: ['완료', '미완료'],
                datasets: [
                    {
                        data: [bingDone/keyTotal, (keyTotal-bingDone)/keyTotal],
                        datalabels: percentLabelOption
                    }
                ]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Bing 검색 진행 상황',
                        font: { family: 'Pretendard', size: 14 }
                    },
                    legend: { position: 'bottom' }
                },
            }
        });

        let expose = new Chart(document.getElementById("exposestate-chart"), {
            type: 'radar',
            data: {
                labels: ['로그인', '관리자', '파일', '불필요', 'GitHub'],
                datasets: []
            },
            options: {
                scales: {
                    r: { ticks: { display: false } }
                },
                plugins: {
                    legend: { position: 'bottom' }
                },
            }
        });

        data.slice(1).forEach(data => {
            var newDataset = {
                label: data[0],
                data: data.slice(3),
                borderWidth: 1,
                fill: true
            }
            expose.data.datasets.push(newDataset);
        }); expose.update();

    }); //END of GET
}

function loadInitiateResults(_reset, pagename) {
    if (loading) return;
    loading = true;

    let tag = '';
    if(pagename == "/fileparses" || pagename == "/neednot") {
        if($(".top-align-box").find(".active").text() != undefined) {
            tag = $(".top-align-box").find(".active").text();
            switch(tag) {
                case "기타": tag = 'others'; break;
                case "에러 페이지": tag = "error"; break;
                case "샘플 페이지": tag = "sample"; break;
                case "서버 정보 노출": tag = "servinfo"; break;
            }
        }
    }

    $.get(pagename + '/default', { tag: tag, page: page }, function(data) {
        $('#results').empty();
        $('#results').append(data);
        $('#loading').hide();

        var count = $('#count-result').text();
        $('.top-total strong').text(count);

        searchMenu(); foldableButton(); pagingButtons();

        loading = false;
        $('#page-' + String(page)).addClass('active');
    });
}

function loadResults(_reset, pagename) {
    if (loading) return;
    loading = true;

    const menu = $('#search-param').val();
    const query = $('#searchInput').val();
    
    let tag = '';
    let param;

    if(pagename == "/fileparses" || pagename == "/neednot") {
        if(pagename === "/fileparses") {
            switch(menu) {
                case "파일 이름": param = 'title'; break;
                case "주요 데이터": param = 'parsed_data'; break;
                default: param = '';
            }}
        if($(".top-align-box").find(".active").text() != undefined) {
            tag = $(".top-align-box").find(".active").text();
            switch(tag) {
                case "기타": tag = ''; break;
                case "에러 페이지": tag = "error"; break;
                case "샘플 페이지": tag = "sample"; break;
                case "서버 정보 노출": tag = "servinfo"; break;
                default: break;
            }
        }
    }
    
    if(pagename != "/fileparses") {
        switch(menu) {
            case "서브도메인": param = 'subdomain'; break;
            case "제목": param = 'title'; break;
            case "URL": param = 'url'; break;
            case "콘텐츠": param = 'content'; break;
            default: param = '';
        }
    }

    if (query != '') {
        $.get(pagename + "/result", { tag: tag, menu: param, key: query, page: page }, function(data) {
            $('#results').empty();
            $('#results').append(data);
            $('#loading').hide();

            var count = $('#count-result').text();
            $('.top-total strong').text(count);

            searchMenu(); foldableButton(); pagingButtons();

            loading = false;
            $('#page-' + String(page)).addClass('active');
        });
    } else {
        $.get(pagename + '/default', { tag: tag, page: page }, function(data) {
            $('#results').empty();
            $('#results').append(data);
            $('#loading').hide();
    
            var count = $('#count-result').text();
            $('.top-total strong').text(count);
    
            searchMenu(); foldableButton(); pagingButtons();
    
            loading = false;
            $('#page-' + String(page)).addClass('active');
        });
    }
}
