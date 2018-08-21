function redirect(URL)
{ 
	parent.frames.home.location.href = URL
}

function isValidURL(url)
{
    var RegExp = /^(\/([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)*(\?(&?([-+_~.\d\w]|%[a-fA-f\d]{2,2})=?)*)?(#([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)?$/;
    if(RegExp.test(url)){
        return true;
    }else{
        return false;
    }
}
 
function parseQuery()
{
	var querystr
	var queryindex
	querystr = "" + parent.parent.document.location.href

	if ((queryindex = querystr.indexOf('?')) != -1)
	{
		querystr = querystr.substring(queryindex + 1)
		
		if ((queryindex = querystr.indexOf('redirect=')) != -1)
		{
			querystr = querystr.substring(queryindex + 9)	
			if (isValidURL(querystr) && (querystr != this.location.pathname))
			{ 
				redirect (querystr)
			}
		
		}
		else	// invalid query string
			alert("Invalid Query String")
	}
}

function frame_check()
{

	if (top == self)

	{
		var newUrl = "/index.html?redirect=" + document.location.pathname;
		var replaceOK = true;
	
		if (navigator.appName.indexOf("Microsoft") > -1)
		{	
			if (parseInt(navigator.appVersion) < 4)
			{	
				replaceOK = false;
			}
		}
	
		if (replaceOK)
		{
			location.replace(newUrl);
		} 
		else
		{
			document.location.href = newUrl;
		}	
	}

	if (self){
		if (self.name == "home") {
			top.frames.home.focus();
		}
	}
}

function highlightTree(url)
{
  var treeframe= parent.frames.navtree;

  if (treeframe.highlighted != 0)
  {
        treeframe.overColor(treeframe.highlighted, "#bcbcbc");
  }
 
  var treeobj= treeframe.document.getElementById(url);

  treeframe.overColor(treeobj, "#dedede");
  treeframe.highlighted= treeobj;
}
