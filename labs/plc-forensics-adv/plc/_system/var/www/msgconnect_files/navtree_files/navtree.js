function highlightView(current)
{
  if (highlighted != 0)
  {
        overColor(highlighted, "#bcbcbc");
  }
 
  overColor(current, "#dedede");
  highlighted= current;
  
  if (eval("typeof(parent.timeoutPntr)") != 'undefined') // clear any pending refreshes from another page
  	parent.window.clearTimeout(parent.timeoutPntr);
}

function showBranch(branch)
{
  var objBranch;
  objBranch = document.getElementById(branch).style
  
  if (objBranch.display == "block")
  {
    objBranch.display="none";
  }
  else
  {
    objBranch.display="block";
  }

  top.frames.home.focus();
}

function branchState(branch, state)
{
  objBranch = document.getElementById(branch).style
  
  if (state == "expand")
  {
    objBranch.display="block";
  }
  else
  {
    objBranch.display="none";
  }
}
function swapFolder(img)
{
  objImg = document.getElementById(img);
  
  if (objImg.src.indexOf('/images/folder.gif') > -1)
  {
    objImg.src = openImg.src;
  }
  else
  {
    objImg.src = closedImg.src;
  }
}

function folderState(img, state)
{
  objImg = document.getElementById(img);
  if (state == "expand")
  {
    objImg.src = openImg.src;
  }
  else
  {
    objImg.src = closedImg.src;
  }
}

function overColor(object, color)
{ 
  object.style.backgroundColor= color;
}

function outColor(object, color)
{  

  if (object == highlighted)
  {
	color= "#dedede";
  }
  
  object.style.backgroundColor= color;
}

function changeAll(state)
{
  // change all folder images
  folderState("f_data_views", state);
  folderState("f_diagnostics", state);
  folderState("f_admin_settings", state);
    folderState("f_device_config", state);
    folderState("f_user_manage", state);
    folderState("f_server_manage", state);
  folderState("f_adv_diagnostics", state);
    folderState("f_enet_ip", state);
    folderState("f_network", state);
    folderState("f_controlbus", state);
    folderState("f_misc", state);
    
  // expand all branches
  branchState("b_data_views", state);
  branchState("b_diagnostics", state);
  branchState("b_admin_settings", state);
    branchState("b_device_config", state);
    branchState("b_user_manage", state);
    branchState("b_server_manage", state);
  branchState("b_adv_diagnostics", state);
    branchState("b_enet_ip", state);
    branchState("b_network", state);
    branchState("b_controlbus", state);
    branchState("b_misc", state);

    top.frames.home.focus();
}
