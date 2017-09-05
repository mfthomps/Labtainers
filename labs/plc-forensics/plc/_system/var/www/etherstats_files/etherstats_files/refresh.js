function jsRefresh()
{
	parent.refreshTime = document.getElementById("refresh").value;
	if (parent.refreshTime != 0)
		document.location.reload();
}

function refreshInit()
{
	if (eval("typeof(parent.refreshTime)") == 'undefined')
		parent.refreshTime = document.getElementById('refresh').value;
	else
		document.getElementById('refresh').value = parent.refreshTime;

	if (eval("typeof(parent.timeoutPntr)") != 'undefined')
		parent.window.clearTimeout(parent.timeoutPntr);

	parent.timeoutPntr = parent.window.setTimeout("frames.home.jsRefresh();", (parent.refreshTime * 1000));
}
