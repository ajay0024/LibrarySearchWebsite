var popoverSettings
$(document).ready(function(dateOptions) {
  $("#search-book").click(function() {
    $("#result").empty()
    if (($("#search-keyword")[0].value).length > 3) {
      // + "&language=" + $("#language")[0].value 
      link = "search_book?search-option=" + $("#search-option")[0].value + "&year=" + $("#year")[0].value + "&search-keyword=" + $("#search-keyword")[0].value
      $("#result").append("<img src='https://c.tenor.com/I6kN-6X7nhAAAAAj/loading-buffering.gif' width='50px'/>")
      $.get(link, function(data) {
        $("#result img").remove();
        console.log(data)
        var jsonObj = $.parseJSON(data);
        console.log(jsonObj)
        if (jsonObj.length == 0) {
          $("#result").append("<h1 class='no-result'>No result returned for your search</h1>")
        }
        for (d in jsonObj) {
          title = jsonObj[d].Title
          author = jsonObj[d].Author
          year = jsonObj[d].Year
          links = jsonObj[d].links
          $("#result").append("<p class='book-details'><span class='title'>" + title + "</span>  <span class='author'> by " + author + "</span> <span class='year'> in " + year + "</span></p>");
          newUl = $("#result").add("ul");
          for (link in links) {
            console.log(link);
            new_li = "<li><a href='" + links[link] + "'>" + link + "</a></li>"
            newUl.append(new_li);
          }
        }
      });
    } else {
      alert("You need to add title or author name for search and number of characters of query should be more than 3")
    }
  });
  $("#search-option").on('change', function() {
    if (this.value=="title"){
      $("#search-keyword").attr("placeholder", "Title");
    }
    else if (this.value=="author") {
      $("#search-keyword").attr("placeholder", "Author");
    }
  });
});
