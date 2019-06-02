const newLocal = 'TEjJuVrFKrd8mlNlAjejnT79Q6OTLNtu';
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');
    var nytKey = newLocal; //defined outside this file
    
    console.log(nytKey);

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview
    var streetStr = $('#street').val();
    var cityStr = $('#city').val();
    var mapAddr = streetStr + ', ' + cityStr;
    
    var htmlUrl = 'http://maps.googleapis.com/maps/api/streetview?size=600x300&location='
    htmlUrl = htmlUrl.concat('\'',mapAddr,'\'');
    
    $greeting.text('Welcome to ' + mapAddr)
    //console.log(htmlUrl);
    $body.append('<img class="bgimg" src="' + htmlUrl + '"/>');

    // Pull NYTimes articles about the location from the NYTDevelopers site
    // sample https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date=01012019&end_date=01012019&facet=false&q=atlanta%20AND%20'14%20main%20street'&sort=newest&api-key=[YOUR_API_KEY]
   
    var nytUrl = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q=';
    nytUrl += encodeURI(cityStr) + '&api-key=' + nytKey;
    console.log(encodeURI(cityStr) + "***" + nytUrl);
    $.getJSON(nytUrl, function(data) {
        $nytHeaderElem.text('New York Time Articles About ' + cityStr);
        
        //console.log('data:' + data)
        var items = [];
        var articles = [];
        articles = data.response.docs; 
        for (i in articles) {
            //alert(articles.length + " " + articles[0].web_url);       
            webUrl = [];
            snippet = [];
            headline = [];
            $.each( articles[i], function( key, val ) {
                //console.log('key:'+key+' value:'+val);
                switch(key) {
                    case 'web_url':
                        webUrl = val;
                        break;
                    case 'snippet':
                            snippet = val;
                        break;
                    case 'headline':
                        headline = val.main;
                        break;
                    //default is to ignore 
                } // switch  
            }) // each
            //alert(webUrl+"****"+headline+"****"+snippet);
            var articleHtml = [];
            articleHtml = "<li class='article'>";
            articleHtml +=   "<a href='" + webUrl + "'>" + headline + "</a>";
            articleHtml +=   "<p>" + snippet + "</p></li>";
            //alert(articleHtml);
            items.push( articleHtml );   
        };
        //alert(items);
        // push items into HTML page
        $('#nytimes-articles').append(items);
    }).error(function(e) {
        $nytHeaderElem.text('New York Time Articles Could Not Be Loaded.');
    });


    // pull wikipedia links
    // URL = https://en.wikipedia.org/w/api.php
    var wikiUrl = "https://en.wikipedia.org/w/api.php?";
    wikiUrl += "format=json&action=opensearch&";
    wikiUrl += "search='" + cityStr + "'&callback=wikiCallback";
    console.log(wikiUrl);
    
    // since jsonp has no error() method, can use a timeout ability to trap errors.
    // The page will not return data if there is an error. value in milliseconds.
    var wikiTimeout = setTimeout(function() {
        $wikiElem.text("Failed to get a wikipedia resourse.");
    }, 8000);

    $.ajax({
        "url" : wikiUrl,
        "dataType" : "jsonp",
        //"prop" : "extracts|links", 
        "success": function (result) {
            //console.log(JSON.stringify(result));
            // article list is in array[1]. The article name is a URL to the article
            var articleList = result[1]; 
            for (var i = 0; i < articleList.length; i++) {
                console.log(i+"****"+articleList[i]);
                var articleStr = articleList[i];
                var articleUrl = "http:/en.wikipedia.org/wiki/" + encodeURI(articleStr);
                $wikiElem.append("<li><a href='" + articleUrl + "'>" +
                                  articleStr + "</a></li>");
            };

            // clear the timeout since values were return before timeout occurred
            clearTimeout(wikiTimeout);
        }
      }).done(function() {
        alert( "done" );
      });

    return false;
};


function answer_from_course_to_find_articles_loop() {
    var nytimesUrl = 'same string from my answer';
    $.getJSON(nytimesUrl, function(data) {
        //assign nytHeaderElem.text()..
        articles = data.response.docs;
        // loop through articles and pull the wanted elements
        for (var i=0; i<articles.length; i++) {
            var article = articles[i];
            $nytElem.append('<li class="article">' +
                            '<a href="' + article.web_url + '">' +
                            article.headline.main + '</a>' + 
                            '<p>' + article.snippet + '</p>' + 
                            '</li>');
        };
    });
}


$('#form-container').submit(loadData);

// loadData();
