function jsConfirm(msg_text) { return confirm(msg_text); }

function URLvalidate(url) {
  var re = /^\/([^\\:\*\?"<>\|\/]{1,80}\/){0,63}([^\\:\*\?"<>\|\/]{1,80})?$/;
  if (re.test(url)) {
    return true;
  } else {
    alert("The URL appears invalid. A filename must not contain any of the following characters:\n\\ / : * ? < > |\n\nA valid URL begins with a leading slash (/), must contain fewer than 64 path segments, and each segment must be less than or equal to 80 characters in length.");
    return false;
  }
}

function addrValidate(address, addrType)
{
	ipArray = new Array(4);

	var re = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
	if (re.test(address)) {
		var parts = address.split(".");

		if ((parseInt(parseFloat(parts[0])) == 0)&&(addrType != "GW")) { return false; }

		for (var i=0; i<parts.length; i++) {
			if ((parseInt(parseFloat(parts[i])) > 255)||(parts[i] != Math.abs(parts[i]))) { return false; }// no negative numbers 
	}

		if ((addrType == "IP") || (addrType == "NS"))	// ip, gateway, nameserver have first octet restrictions
	{
			if((parseInt(parseFloat(parts[0])) == 0) || (parseInt(parseFloat(parts[0])) == 127) || (parseInt(parseFloat(parts[0])) > 223))
				{ return false; }
	}
		return true;}
	else {
		if((addrType == "GW") || (addrType == "NS"))
	{
			return true;	// blank gateway or nameservers is valid.			
	}
		else
		{
			return false;
		}
		}
		}

function isValidIP (ipaddr)
{
	var re = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
	if (re.test(ipaddr)) {
		var ipArray = ipaddr.split(".");
		if (parseInt(parseFloat(ipArray[0])) == 0) { return false; }
		for (var i=0; i<ipArray.length; i++) {
			if ((parseInt(parseFloat(ipArray[i])) > 255)||(ipArray[i] != Math.abs(ipArray[i]))) { return false; }// no negative numbers 
	}
	if (ipArray[0] < 128) {
		if (ipArray[0] == 0 || (ipArray[1] == 0 && ipArray[2] == 0 && ipArray[3] == 0)) return false;		// host or network all zeros
		if (ipArray[1] == 255 && ipArray[2] == 255 && ipArray[3] == 255) return false;		// host is all ones
		if (ipArray[0] == 127) return false;	// network is all ones
	} else if (ipArray[0] < 192) {
		if ((ipArray[0] = 128 && ipArray[1] == 0) || (ipArray[2] == 0 && ipArray[3] == 0)) return false;		// host or network all zeros
		if (ipArray[2] == 255 && ipArray[3] == 255) return false;		// host is all ones
		if (ipArray[0] == 191 && ipArray[1] == 255) return false;	// network is all ones
	} else if (ipArray[0] < 224) {
		if ((ipArray[0] == 192 && ipArray[1] == 0 && ipArray[2] == 0) || ipArray[3] == 0) return false;		// host or network all zeros
		if (ipArray[3] == 255) return false;		// host is all ones
		if (ipArray[0] == 223 && ipArray[1] == 255 && ipArray[2] == 255) return false;	// network is all ones
	} else return false;	// Unsupported address class
		return true;}
	else {
		return false;
	}
}

function isValidSubnet (subnetAddr)
{
	var i, subnet = 0;
	var mask = 0x00000001, count = 1;


	var re = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
	if (re.test(subnetAddr)) {
		var ipArray = subnetAddr.split(".");

		if (parseInt(parseFloat(ipArray[0])) == 0) { return false; }

		for (var i=0; i<ipArray.length; i++) {
			if ((parseInt(parseFloat(ipArray[i])) > 255)||(ipArray[i] != Math.abs(ipArray[i]))) { return false; }// no negative numbers 
		subnet |= (parseInt(parseFloat(ipArray[i])) << (8 * (3 - i)));
	}


	done = false;
	for (i=0; i<4; i++) {
		if (ipArray[i] == 255) {
			if (done) return false;
		} else if ((ipArray[i] == 254) || (ipArray[i] == 252) || (ipArray[i] == 248) || (ipArray[i] == 240) || (ipArray[i] == 224) || (ipArray[i] == 192) || (ipArray[i] == 128)) {
			if (!done) done = true;
			else return false;
		} else if (ipArray[i] == false) {
			if (!done) done = true;
		} else {
			return false;
		}
	}

		return true;}
	else {
		return false;
	}

}

function isValidEmail(emailAddr) 
{
	var regexpr = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    
	return regexpr.test(emailAddr);
}

function isValidHostname(hostname) {
	var regexpr = /^[a-zA-Z]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$/
    
	return regexpr.test(hostname);
}
