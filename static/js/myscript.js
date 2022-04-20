var popoverSettings
$(document).ready(function(dateOptions) {
  $("#search-book").click(function() {
    $("#result").empty()
    if (($("#title")[0].value).length >3 || ($("#author")[0].value).length >3) {
      link = "search_book?title=" + $("#title")[0].value + "&language=" + $("#language")[0].value + "&year=" + $("#year")[0].value+ "&author=" + $("#author")[0].value
      $("#result").append("<img src='https://c.tenor.com/I6kN-6X7nhAAAAAj/loading-buffering.gif' width='50px'/>")
      $.get(link, function(data) {
        $("#result img").remove();
        var jsonObj = $.parseJSON(data);
        console.log(jsonObj)
        if (jsonObj.length==0){
          $("#result").append("<h1 class='no-result'>No result returned for your search</h1>")
        }
        for (d in jsonObj) {
          title = jsonObj[d].Title
          author = jsonObj[d].Author
          year = jsonObj[d].Year
          links = jsonObj[d].links
          $("#result").append("<p class='book-details'><span class='title'>" + title + "</span>  <span class='author'> by " + author + "</span> <span class='year'> in " + year + "</span></p>");
          newUl=$("#result").add("ul");
          for (link in links) {
            console.log(link);
            new_li = "<li><a href='" + links[link] + "'>" + link + "</a></li>"
            newUl.append(new_li);
          }

        }
        // $("#result").html(d);

      });
    } else {
      alert("You need to add title or author name for search and number of characters of query should be more than 3")
    }
  });
});
