var Browser = {
	IE:     !!(window.attachEvent && !window.opera),
	Opera:  !!window.opera,
	WebKit: navigator.userAgent.indexOf('AppleWebKit/') > -1,
	Gecko:  navigator.userAgent.indexOf('Gecko') > -1 && navigator.userAgent.indexOf('KHTML') == -1,
	MobileSafari: !!navigator.userAgent.match(/Apple.*Mobile.*Safari/)
};

function XMLDocument() {
	if (Browser.IE)
	{
//		var names = ["Msxml2.DOMDocument.6.0", "Msxml2.DOMDocument.3.0", "MSXML2.DOMDocument", "MSXML.DOMDocument", "Microsoft.XMLDOM"];
		var names = ["MSXML4.DOMDocument", "MSXML3.DOMDocument", "MSXML2.DOMDocument", "MSXML.DOMDocument", "Microsoft.XmlDom"];
		for (var key in names) {
			try {
				return new ActiveXObject(names[key])
			} catch (e) {}
		}
		throw new Error('Unable to create XMLDocument');
	}
	else
	{
		if (!(this instanceof XMLDocument)) return new XMLDocument();

		this.__proto__ = document.implementation.createDocument("", "", null);

		if (!this.xml)
		{
			this.__defineGetter__("xml", function(){
				return new XMLSerializer().serializeToString(this);
			});
		}

		if (!this.setProperty)
		{
			this.setProperty = function(name, val) {
				switch(name)
				{
					case "SelectionNamespaces":
						var re = /xmlns:(.*)=('|")(.*)('|")/;
						var res = re.exec(val);
						if (null != res)
						{
							var pre = res[1];
							var uri = res[3];
							if (null == this.namespaces) this.namespaces = new Array();
							if (null == this.makeNSResolver) this.makeNSResolver = function(ns, dnsr) {
								return function(prefix) {
									return ns[prefix] || dnsr(prefix);
								}
							};
							this.namespaces[pre] = uri;
						}
						break;

					case "SelectionLanguage":
						if (val != "XPath") throw new Error("Unsupported value \"" + val + "\" for property \"" + name + "\"");
						break;

					default:
						throw new Error("Unknown property \"" + name + "\" passed to setProperty");
				}
			}
		}

		if (!this.createNode)
		{
			this.createNode = function(type, name, ns) {
				switch (type)
				{
					case Node.ELEMENT_NODE:
						return this.createElementNS(ns, name);
						break;

					case Node.ATTRIBUTE_NODE:
						return this.createAttributeNS(ns, name);
						break;

					case Node.TEXT_NODE:
					case Node.CDATA_SECTION_NODE:
					case Node.ENTITY_REFERENCE_NODE:
					case Node.ENTITY_NODE:
					case Node.PROCESSING_INSTRUCTION_NODE:
					case Node.COMMENT_NODE:
					case Node.DOCUMENT_NODE:
					case Node.DOCUMENT_TYPE_NODE:
					case Node.DOCUMENT_FRAGMENT_NODE:
					case Node.NOTATION_NODE:
						throw new Error("Unimplemented...");
						break;

					default:
						throw new Error("Unknown node type!");
				}
			};
		}
	}
};

// Just in case IE doesn't have it...
if (typeof(Node) == "undefined") { Node = new Object(); }

if (!Node.ELEMENT_NODE) {
	// DOM level 2 ECMAScript Language Binding
	Node.ELEMENT_NODE = 1;
	Node.ATTRIBUTE_NODE = 2;
	Node.TEXT_NODE = 3;
	Node.CDATA_SECTION_NODE = 4;
	Node.ENTITY_REFERENCE_NODE = 5;
	Node.ENTITY_NODE = 6;
	Node.PROCESSING_INSTRUCTION_NODE = 7;
	Node.COMMENT_NODE = 8;
	Node.DOCUMENT_NODE = 9;
	Node.DOCUMENT_TYPE_NODE = 10;
	Node.DOCUMENT_FRAGMENT_NODE = 11;
	Node.NOTATION_NODE = 12;
}

if (!Browser.IE) {
	if (!Node.prototype.transformNode)
	{
		Node.prototype.transformNode = function (oXslDom) {
			var oProcessor = new XSLTProcessor();
			oProcessor.importStylesheet(oXslDom);
			var oResultDom = oProcessor.transformToDocument(this);
			var sResult = new XMLSerializer().serializeToString(oResultDom);
			if (sResult.indexOf("<transformiix:result") > -1) {
				sResult = sResult.substring(sResult.indexOf(">") + 1, sResult.lastIndexOf("<"));
			}
			return sResult;
		};
	}

	if (!Node.prototype.selectNodes)
	{
		Node.prototype.selectNodes = function(path) {
			var nsr;
			var xr;
			if (this.ownerDocument)
			{
				if (null != this.ownerDocument.makeNSResolver)
					nsr = this.ownerDocument.makeNSResolver(this.ownerDocument.namespaces, this.ownerDocument.createNSResolver(this.ownerDocument.documentElement));
				else
					nsr = this.ownerDocument.createNSResolver(this.ownerDocument.documentElement);
				xr = this.ownerDocument.evaluate(path, this, nsr, XPathResult.ANY_TYPE, null);
			}
			else
			{
				if (null != this.makeNSResolver)
					nsr = this.makeNSResolver(this.namespaces, this.createNSResolver(this.documentElement));
				else
					nsr = this.createNSResolver(this.documentElement);
				xr = this.evaluate(path, this, nsr, XPathResult.ANY_TYPE, null);
			}
			var ret = new Object();

			var txr = xr.iterateNext();
			var i = 0;
			while (txr)
			{
				ret[i] = txr;
				txr = xr.iterateNext();
				i = i + 1;
			}
			ret.length = i;
			ret.item = function(n) { return this[n]; };
			return ret;
		};
	}

	Node.prototype.selectSingleNode = function(path) {
		var nodes = this.selectNodes(path);
		if (nodes.length > 0)
			return nodes.item(0);
		else
			return null;
	}
}

if (!Browser.IE && !Browser.Gecko)
{
	alert("Creating/editing a data view requires Internet Explorer 5.5 or greater with XML support, or Firefox 2 or greater. Please upgrade your browser or load the appropriate patches to support XML.");
	history.go(-1);
}

  var newRoot;
  var xmlDoc;
  var xslDoc;

  var nodes;
  var node;

  var rowcolor = "#dedede";
  var PATH_TO_LOCAL_BACKPLANE = "1,";

  var DATAVIEW_NAMESPACE = "";
  var DATATYPES_NAMESPACE = "";
  var XSI_NAMESPACE = "http://www.w3.org/2001/XMLSchema-instance";

function initialize(fname) {
  xmlDoc = new XMLDocument();
  xmlDoc.async = false;
  xmlDoc.setProperty("SelectionLanguage", "XPath");

  xslDoc = new XMLDocument();
  xslDoc.async = false;

  /* Turn on the wait cursor */
  document.body.style.cursor = "wait";

  if (fname == "") {
    var pi = xmlDoc.createProcessingInstruction("xml", "version=\"1.0\"");
    xmlDoc.appendChild(pi);

    pi = xmlDoc.createProcessingInstruction("xml-stylesheet", "href=\"/dataview/dataview.xsl\" type=\"text/xsl\"");
    xmlDoc.appendChild(pi);

    newRoot = xmlDoc.createNode(Node.ELEMENT_NODE, "view", DATAVIEW_NAMESPACE);

    if (Browser.Gecko)
    {
      // Firefox doesn't properly add the namespace declaration for this prefix, so we'll add it ourselves.
      attribute = xmlDoc.createAttribute("xmlns:xsi");
      attribute.value = XSI_NAMESPACE;
      newRoot.attributes.setNamedItem(attribute);
    }
    
    attribute = xmlDoc.createNode(Node.ATTRIBUTE_NODE, "xsi:schemaLocation", XSI_NAMESPACE);
    attribute.value = DATAVIEW_NAMESPACE + " /schema/dataview.xsd";
    newRoot.attributes.setNamedItem(attribute);

    attribute = xmlDoc.createAttribute("xmlns:cip");
    attribute.value = DATATYPES_NAMESPACE;
    newRoot.attributes.setNamedItem(attribute);

    attribute = xmlDoc.createAttribute("name");
    attribute.value = '';
    newRoot.attributes.setNamedItem(attribute);

    attribute = xmlDoc.createAttribute("description");
    attribute.value = '';
    newRoot.attributes.setNamedItem(attribute);

    xmlDoc.appendChild(newRoot);
    xmlDoc.setProperty("SelectionNamespaces", "xmlns:dv='" + DATAVIEW_NAMESPACE + "'");
  } else {
    try {
      xmlDoc.load(fname);
      xmlDoc.setProperty("SelectionNamespaces", "xmlns:dv='" + DATAVIEW_NAMESPACE + "'");
      if (!isValidDataView(xmlDoc)) {
        alert("The dataview '" + fname + "' is not valid and could not be loaded. Please delete the view and recreate it.");
        history.go(-1);
        return;
      }
      newRoot = xmlDoc.documentElement;
      description.value = newRoot.attributes.getNamedItem("description").nodeValue;
      dataview.value = newRoot.attributes.getNamedItem("name").nodeValue;
      form1.xmlname.value = dataview.value;
      document.form1.oldname.value = fname.substring(fname.lastIndexOf("/")+1);
      document.form1.oldcount.value = xmlDoc.selectNodes("/dv:view/dv:tag").length;
    } catch (exc) {
      alert("The dataview '" + fname + "' is malformed and could not be loaded. Please delete the view and recreate it.");
      history.go(-1);
      return;
    }
  }

  xslDoc.load("/dataview/newview.xsl")

  document.getElementById("island").innerHTML = xmlDoc.documentElement.transformNode(xslDoc)

  document.getElementById("slot").value = '';
  document.getElementById("tagname").value = '';
  document.getElementById("datatype").value = 2;
  document.getElementById("displaytype").value = 0;
  document.getElementById("readwrite").value = 0;

  /* Restore the default cursor */
  document.body.style.cursor = "default";
}

function isValidDataView(xmlDoc) {
  /*
   * There must be one and only one root "view" node
   */

  var elts_view = xmlDoc.selectNodes("/dv:view");
  if (elts_view.length == 1) {

    /*
     * The root "view" node must have a name and description
     */
    var elt_view = xmlDoc.selectSingleNode("/dv:view");
    if (elt_view.attributes.getNamedItem("name") && elt_view.attributes.getNamedItem("description")) {

      /*
       * Get all the tag elements
       */
      var elts_tag = xmlDoc.selectNodes("/dv:view/dv:tag");
      for (i=0; i<elts_tag.length; i++) {

        /*
         * A tag element must have "name", "valueType", "path", "display", and "access" attributes
         */
        if (elts_tag[i].attributes.getNamedItem("name") &&
            elts_tag[i].attributes.getNamedItem("valueType") &&
            elts_tag[i].attributes.getNamedItem("path") &&
            elts_tag[i].attributes.getNamedItem("display") &&
            elts_tag[i].attributes.getNamedItem("access")) {

          /*
           * A tag must have one and only one child "value" element
           */
          if (xmlDoc.selectNodes("/dv:view/dv:tag[@name='" + elts_tag[i].attributes.getNamedItem("name").nodeValue + "' and @path='" + elts_tag[i].attributes.getNamedItem("path").nodeValue + "' and @valueType='" + elts_tag[i].attributes.getNamedItem("valueType").nodeValue + "']/dv:value").length == 1) {
            /*
             * A tag must not have a duplicate
             */
            if (xmlDoc.selectNodes("/dv:view/dv:tag[@name='" + elts_tag[i].attributes.getNamedItem("name").nodeValue + "' and @path='" + elts_tag[i].attributes.getNamedItem("path").nodeValue + "']").length != 1) {
              return false;
            }
          } else return false;
        } else return false;
      }

      /*
       * If we made it through the for loop, everything is good
       */
      return true;

    } else return false;
  } else return false;
}

function add_row() {
  var newNode
  var newChild

  if (document.getElementById("slot").value == "") {
    alert("Please supply a controller slot!");
    document.getElementById("slot").focus();
    return;
  }

  if (document.getElementById("tagname").value == "") {
    alert("Please supply a tag name!");
    document.getElementById("tagname").focus();
    return;
  }

  /* Path validation */
  if (!isValidSlot(document.getElementById("slot").value)) {
    alert("The slot is invalid. Please enter a\nnumber between 0 and 16, inclusive");
    document.getElementById("slot").focus();
    return;
  }

  /* No BOOL arrays... */
  if ((parseInt(document.getElementById("datatype").value) == 0) && (document.getElementById("tagname").value.indexOf("[") != -1) && (document.getElementById("tagname").value.indexOf("]") != -1) && (document.getElementById("tagname").value.indexOf("[") < document.getElementById("tagname").value.indexOf("]"))) {
    alert("Boolean arrays are not supported. Consult the release notes for more information.");
    document.getElementById("tagname").focus();
    return;
  }

  document.getElementById("slot").value = "" + parseInt(document.getElementById("slot").value);

  if (xmlDoc.selectNodes("/dv:view/dv:tag[@path='" + PATH_TO_LOCAL_BACKPLANE + document.getElementById("slot").value + "' and @name='" + document.getElementById("tagname").value + "']").length > 0) {
    alert("A tag with this slot and name already exists. Please supply a different slot or tag name.");
    document.getElementById("slot").focus();
    return;
  }

  document.getElementById("addrow").title = "Add this tag";
  document.getElementById("addsave").innerHTML = "Add";
  document.getElementById("canceldiv").innerHTML = "";
  document.getElementById("cancelrow").style.display = "none";

  newNode = xmlDoc.createNode(Node.ELEMENT_NODE, "tag", DATAVIEW_NAMESPACE);

  newChild = xmlDoc.createAttribute("name")
  newChild.value = document.getElementById("tagname").value
  document.getElementById("tagname").value = ''
  newNode.attributes.setNamedItem(newChild)

  newChild = xmlDoc.createAttribute("valueType")
  switch (parseInt(document.getElementById("datatype").value)) {
    case 0:
      newChild.value = "cip:dt_BOOL"
      break;
    case 1:
      newChild.value = "cip:dt_SINT"
      break;
    case 2:
      newChild.value = "cip:dt_INT"
      break;
    case 3:
      newChild.value = "cip:dt_DINT"
      break;
    case 4:
      newChild.value = "cip:dt_REAL"
      break;
    case 5:
      newChild.value = "cip:dt_STRINGI"
  }
  document.getElementById("datatype").value = 2
  newNode.attributes.setNamedItem(newChild)

  newChild = xmlDoc.createAttribute("path")
  newChild.value = PATH_TO_LOCAL_BACKPLANE + document.getElementById("slot").value
  document.getElementById("slot").value = ''
  newNode.attributes.setNamedItem(newChild)

  newChild = xmlDoc.createAttribute("display")
  switch(parseInt(document.getElementById("displaytype").value)) {
    case 0:
      newChild.value = "Decimal";
      break;
    case 1:
      newChild.value = "Hexadecimal";
      break;
    case 2:
      newChild.value = "Octal";
      break;
    case 3:
      newChild.value = "Binary";
      break;
    case 4:
      newChild.value = "String";
  }
  document.getElementById("displaytype").value = 0
  document.getElementById("displaytype").disabled = false
  newNode.attributes.setNamedItem(newChild)

  newChild = xmlDoc.createAttribute("access")
  if (document.getElementById("readwrite").value == 0) {
    newChild.value = "admin"
  } else if (document.getElementById("readwrite").value == 1) {
    newChild.value = "write"
  } else {
    newChild.value = "read"
  }
  document.getElementById("readwrite").value = 0
  newNode.attributes.setNamedItem(newChild)

  /* Stick in a nil value node to be a valid document */
  var newValueNode = xmlDoc.createNode(Node.ELEMENT_NODE, "value", DATAVIEW_NAMESPACE);
  var newNil = xmlDoc.createNode(Node.ATTRIBUTE_NODE, "xsi:nil", XSI_NAMESPACE);
  newNil.value = "true";
  newValueNode.attributes.setNamedItem(newNil);

  newNode.appendChild(xmlDoc.createTextNode("\n\t\t"));
  newNode.appendChild(newValueNode);
  newNode.appendChild(xmlDoc.createTextNode("\n\t"));
  newRoot.appendChild(xmlDoc.createTextNode("\n\t"));
  newRoot.appendChild(newNode);
  
  document.getElementById("island").innerHTML = xmlDoc.documentElement.transformNode(xslDoc)
  document.getElementById("slot").focus()
}

function do_row() {
  /* Turn on the wait cursor */
  document.body.style.cursor = "wait";
  setTimeout("do_row2();", 10);
}

function do_row2() {
  if ((document.getElementById("e_slot").value == "" ) && (document.getElementById("e_tag").value == "")) {
    add_row();
  } else {
    nodes = xmlDoc.selectNodes("/dv:view/dv:tag[@path='" + document.getElementById("e_slot").value + "' and @name='" + document.getElementById("e_tag").value + "']");
    if (nodes.length > 0) {
      node = nodes.item(0);
      save_row();
    } else {
      add_row();
    }
  }
  /* Restore the cursor cursor */
  document.body.style.cursor = "default";
}

function save_row() {
  var newChild

  if (document.getElementById("slot").value == "") {
    alert("Please supply a controller path!");
    return;
  }

  if (document.getElementById("tagname").value == "") {
    alert("Please supply a tag name!");
    return;
  }

  /* Path validation */
  if (!isValidSlot(document.getElementById("slot").value)) {
    alert("The slot is invalid. Please enter a\nnumber between 0 and 16, inclusive");
    document.getElementById("slot").focus();
    return;
  }

  /* No BOOL arrays... */
  if ((parseInt(document.getElementById("datatype").value) == 0) && (document.getElementById("tagname").value.indexOf("[") != -1) && (document.getElementById("tagname").value.indexOf("]") != -1) && (document.getElementById("tagname").value.indexOf("[") < document.getElementById("tagname").value.indexOf("]"))) {
    alert("Boolean arrays are not supported. Consult the release notes for more information.");
    document.getElementById("tagname").focus();
    return;
  }

  document.getElementById("slot").value = "" + parseInt(document.getElementById("slot").value);

  if ((PATH_TO_LOCAL_BACKPLANE + document.getElementById("slot").value == document.getElementById("e_slot").value) && (document.getElementById("tagname").value == document.getElementById("e_tag").value)) {
    /* The slot and tag name are the same as they were before, so the "limit" of the number of matching
       nodes in the document is 1 (the one that previously existed) */
    xpathLimit = 1;
  } else {
    /* This isn't the same as before, so there should be none that match */
    xpathLimit = 0;
  }

  if (xmlDoc.selectNodes("/dv:view/dv:tag[@path='" + PATH_TO_LOCAL_BACKPLANE + document.getElementById("slot").value + "' and @name='" + document.getElementById("tagname").value + "']").length > xpathLimit) {
    alert("A tag with this path and name already exists. Please supply a different path or tag name.");
    return;
  }

  document.getElementById("addrow").title = "Add this tag";
  document.getElementById("addsave").innerHTML = "Add";
  document.getElementById("canceldiv").innerHTML = "";
  document.getElementById("cancelrow").style.display = "none";

  node.selectSingleNode("@path").value = PATH_TO_LOCAL_BACKPLANE + document.getElementById("slot").value;
  document.getElementById("slot").value = '';

  node.selectSingleNode("@name").value = document.getElementById("tagname").value;
  document.getElementById("tagname").value = '';

  switch (parseInt(document.getElementById("datatype").value)) {
    case 0:
      node.selectSingleNode("@valueType").value = "cip:dt_BOOL"
      break;
    case 1:
      node.selectSingleNode("@valueType").value = "cip:dt_SINT"
      break;
    case 2:
      node.selectSingleNode("@valueType").value = "cip:dt_INT"
      break;
    case 3:
      node.selectSingleNode("@valueType").value = "cip:dt_DINT"
      break;
    case 4:
      node.selectSingleNode("@valueType").value = "cip:dt_REAL"
      break;
    case 5:
      node.selectSingleNode("@valueType").value = "cip:dt_STRINGI"
  }
  document.getElementById("datatype").value = 2;

  switch(parseInt(document.getElementById("displaytype").value)) {
    case 0:
      node.selectSingleNode("@display").value = "Decimal";
      break;
    case 1:
      node.selectSingleNode("@display").value = "Hexadecimal";
      break;
    case 2:
      node.selectSingleNode("@display").value = "Octal";
      break;
    case 3:
      node.selectSingleNode("@display").value = "Binary";
      break;
    case 4:
      node.selectSingleNode("@display").value = "String";
  }
  document.getElementById("displaytype").value = 0;
  document.getElementById("displaytype").disabled = false;

  if (document.getElementById("readwrite").value == 0) {
    node.selectSingleNode("@access").value = "admin"
  } else if (document.getElementById("readwrite").value == 1) {
      node.selectSingleNode("@access").value = "write"
  } else {
      node.selectSingleNode("@access").value = "read"
  }
  document.getElementById("readwrite").value = 0
	
  document.getElementById("tagtable").rows[parseInt(document.getElementById("e_row").value)].style.backgroundColor = rowcolor;

  document.getElementById("e_slot").value = "";
  document.getElementById("e_tag").value = "";
  document.getElementById("e_row").value = "";

  document.getElementById("island").innerHTML = xmlDoc.documentElement.transformNode(xslDoc)
  document.getElementById("slot").focus()
}

function edit_row(vslot, vtag, tagnum) {
  nodes = xmlDoc.selectNodes("/dv:view/dv:tag[@path='" + vslot + "' and @name='" + vtag + "']");

  if (document.getElementById("e_row").value != "") {
    document.getElementById("tagtable").rows[parseInt(document.getElementById("e_row").value)].style.backgroundColor = rowcolor;
  }

  if (nodes.length > 0) {
    document.getElementById("addrow").title = "Update this tag";
    document.getElementById("addsave").innerHTML = "Update";
    document.getElementById("canceldiv").innerHTML = "Cancel";
    document.getElementById("cancelrow").style.display = "block";

    node = nodes[0];

    document.getElementById("e_slot").value = node.selectSingleNode("@path").value;
    document.getElementById("slot").value = document.getElementById("e_slot").value.substring(PATH_TO_LOCAL_BACKPLANE.length, document.getElementById("e_slot").value.length);
    document.getElementById("tagname").value = node.selectSingleNode("@name").value;
    document.getElementById("e_tag").value = document.getElementById("tagname").value;
    document.getElementById("e_row").value = tagnum;

    switch (node.selectSingleNode("@valueType").value) {
      case "cip:dt_BOOL":
        document.getElementById("datatype").value = 0;
        break;
      case "cip:dt_SINT":
        document.getElementById("datatype").value = 1;
        break;
      case "cip:dt_INT":
        document.getElementById("datatype").value = 2;
        break;
      case "cip:dt_DINT":
        document.getElementById("datatype").value = 3;
        break;
      case "cip:dt_REAL":
        document.getElementById("datatype").value = 4;
        break;
      case "cip:dt_STRINGI":
        document.getElementById("datatype").value = 5;
    }
    if ((parseInt(document.getElementById("datatype").value) == 0) || (parseInt(document.getElementById("datatype").value) == 5)) {
      document.getElementById("displaytype").value = "4";
      document.getElementById("displaytype").disabled = true;
    } else if (parseInt(document.getElementById("datatype").value) == 4) {
      document.getElementById("displaytype").value = "0";
      document.getElementById("displaytype").disabled = true;
    } else {
      switch (node.selectSingleNode("@display").value) {
        case "Decimal":
          document.getElementById("displaytype").value = 0;
          break;
        case "Hexadecimal":
          document.getElementById("displaytype").value = 1;
          break;
        case "Octal":
          document.getElementById("displaytype").value = 2;
          break;
        case "Binary":
          document.getElementById("displaytype").value = 3;
          break;
        case "String":
          document.getElementById("displaytype").value = 4;
      }
      document.getElementById("displaytype").disabled = false;
    }
    if (node.selectSingleNode("@access").value == "admin") {
      document.getElementById("readwrite").value = 0;
    } else if (node.selectSingleNode("@access").value == "write") {
      document.getElementById("readwrite").value = 1;
    } else {
      document.getElementById("readwrite").value = 2;
    }

    /* Color the background of the row under edit */
    rowcolor = document.getElementById("tagtable").rows[tagnum].style.backgroundColor;
    document.getElementById("tagtable").rows[tagnum].style.backgroundColor = "#ffff80";

    document.getElementById("slot").focus()
  }
}

function cancel_row() {
  document.getElementById("tagtable").rows[parseInt(document.getElementById("e_row").value)].style.backgroundColor = rowcolor;

  document.getElementById("e_slot").value = "";
  document.getElementById("e_tag").value = "";
  document.getElementById("e_row").value = "";

  document.getElementById("slot").value = "";
  document.getElementById("tagname").value = "";
  document.getElementById("datatype").value = 2;
  document.getElementById("displaytype").value = 0;
  document.getElementById("displaytype").disabled = false;
  document.getElementById("readwrite").value = 0;

  document.getElementById("addrow").title = "Add this tag";
  document.getElementById("addsave").innerHTML = "Add";
  document.getElementById("canceldiv").innerHTML = "";
  document.getElementById("cancelrow").style.display = "none";

  document.getElementById("slot").focus();
}

function del_row(vslot, vtag, vrow) {
  var dnodes
  var dnode

  dnodes = xmlDoc.selectNodes("/dv:view/dv:tag[@path='" + vslot + "' and @name='" + vtag + "']");

  if (dnodes.length > 0) {
    if ((document.getElementById("e_slot").value != "") && (document.getElementById("e_tag").value != "") && (document.getElementById("e_row").value != "") && (document.getElementById("e_slot").value == vslot) && (document.getElementById("e_tag").value == vtag) && (document.getElementById("e_row").value == vrow)) {
      /* The user is trying to delete the tag we're editing */
      document.getElementById("tagtable").rows[parseInt(document.getElementById("e_row").value)].style.backgroundColor = rowcolor;

      document.getElementById("e_slot").value = "";
      document.getElementById("e_tag").value = "";
      document.getElementById("e_row").value = "";

      document.getElementById("slot").value = "";
      document.getElementById("tagname").value = "";
      document.getElementById("datatype").value = 2;
      document.getElementById("displaytype").value = 0;
      document.getElementById("displaytype").disabled = false;
      document.getElementById("readwrite").value = 0;

      document.getElementById("addrow").title = "Add this tag";
      document.getElementById("addsave").innerHTML = "Add";
      document.getElementById("canceldiv").innerHTML = "";
      document.getElementById("cancelrow").style.display = "none";
    }
    dnode = dnodes.item(0);
    dnode.parentNode.removeChild(dnode);
  }

  document.getElementById("island").innerHTML = xmlDoc.documentElement.transformNode(xslDoc)

  if ((document.getElementById("e_row").value != "") && (parseInt(document.getElementById("e_row").value) != vrow)) {
    if (parseInt(document.getElementById("e_row").value) > vrow) {
      document.getElementById("e_row").value = "" + (parseInt(document.getElementById("e_row").value) - 1);
    }
    rowcolor = document.getElementById("tagtable").rows[parseInt(document.getElementById("e_row").value)].style.backgroundColor;
    document.getElementById("tagtable").rows[parseInt(document.getElementById("e_row").value)].style.backgroundColor = "#ffff80";
  }

  document.getElementById("slot").focus();
}

function update_name() {
  var charect = "";
  var dv = new String (dataview.value);
  var c;
  var viewsDoc;

  for (var n = 1 ; n <= dv.length ; n++) 
  {
    c = dv.substring(n-1,n);
    if (((c >= "a") && (c <= "z")) || ((c >= "A") && (c <= "Z")) || ((c >= "0") && (c <= "9")) || (c == "_"))
    {charect+=c;}
    else if (c == " ")
    {charect+="_";}
  }
  dataview.value = charect;

  form1.xmlname.value = dataview.value;
  return true;
}

function update_description() {

var descriptioncount;
var descriptionstring;

if (document.getElementById('description').value.length > 512 ) 
	{ 
 	descriptioncount = document.getElementById('description').value.length - 512 
 	descriptionstring = descriptioncount + ' character' 
 	if (descriptioncount > 1 ) 
		descriptionstring = descriptionstring + 's'; 
	descriptionstring = descriptionstring + '.   '; 
	alert('Description is limited to 512 characters.  Please remove ' + descriptionstring); 
	document.getElementById('description').focus(); 
	return false; 
	} 
}

function validate() {
  var attribute

  if (newRoot.childNodes.length == 0) {
    alert("Please add tags to the data view before saving!");
    return;
  }

  if (dataview.value == "") {
    alert("Please give the data view a name before saving!");
    return;
  }

  update_name();

  /* See if this view exists, and alert if so */
  if ((document.form1.oldname.value == "") || ((dataview.value + ".xml").toLowerCase() != document.form1.oldname.value.toLowerCase())) {
    viewsDoc = new XMLDocument()
    viewsDoc.async = false;
    viewsDoc.setProperty("SelectionLanguage", "XPath");
    viewsDoc.load("/rokform/DataViewsXML");

    if (viewsDoc.selectSingleNode("/views/view[@name='" + dataview.value + "']")) {
      if (!confirm("WARNING: A data view named '" + dataview.value + "' already exists. Saving with this name will overwrite the existing data view. Are you sure you wish to use this name?")) {
        return;
      }
    }
  }

  // Remove any and all error attributes from tag nodes
  for (i=newRoot.firstChild; i; i=i.nextSibling) {
    if ((i.nodeType == 1) && (i.nodeName == "tag")) {
      if (i.attributes.getNamedItem("error")) {
        i.attributes.removeNamedItem("error");
      }
    }
  }

  attribute = newRoot.attributes.getNamedItem("name");
  attribute.value = dataview.value;

  attribute = newRoot.attributes.getNamedItem("description");
  attribute.value = description.value;
  
  newRoot.appendChild(xmlDoc.createTextNode("\n"));

  document.form1.tagcount.value = xmlDoc.selectNodes("/dv:view/dv:tag").length;
  document.form1.xmltext.value=xmlDoc.xml;
  document.form1.submit();
}

function typeUpdate() {
  if ((parseInt(document.getElementById("datatype").value) == 5) || (parseInt(document.getElementById("datatype").value) == 0)){
    /* String or BOOL data type - change the display as combo box */
    document.getElementById("displaytype").value = "4";
    document.getElementById("displaytype").disabled = true;
  } else if (parseInt(document.getElementById("datatype").value) == 4) {
    /* REAL data type - change the display as combo box */
    document.getElementById("displaytype").value = "0";
    document.getElementById("displaytype").disabled = true;
  } else {
    /* Not a string type - enable the combo box */
    if (document.getElementById("displaytype").disabled) {
      document.getElementById("displaytype").disabled = false;
      document.getElementById("displaytype").value = "0";
    }
  }
}

function validate_displayas() {
  if (((parseInt(document.getElementById("datatype").value) == 1) || (parseInt(document.getElementById("datatype").value) == 2) || (parseInt(document.getElementById("datatype").value) == 3)) && (parseInt(document.getElementById("displaytype").value) == 4)){
    document.getElementById("displaytype").value = 0;
  }
}

function isValidSlot(sl) {
  return ((parseInt(sl) >= 0) && (parseInt(sl) <= 16));
}
