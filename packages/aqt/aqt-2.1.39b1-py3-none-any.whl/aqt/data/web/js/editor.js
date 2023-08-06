"use strict";
/* Copyright: Ankitects Pty Ltd and contributors
 * License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html */
let currentField = null;
let changeTimer = null;
let currentNoteId = null;
/* kept for compatibility with add-ons */
String.prototype.format = function (...args) {
    return this.replace(/\{\d+\}/g, (m) => {
        const match = m.match(/\d+/);
        return match ? args[match[0]] : "";
    });
};
function setFGButton(col) {
    $("#forecolor")[0].style.backgroundColor = col;
}
function saveNow(keepFocus) {
    if (!currentField) {
        return;
    }
    clearChangeTimer();
    if (keepFocus) {
        saveField("key");
    }
    else {
        // triggers onBlur, which saves
        currentField.blur();
    }
}
function triggerKeyTimer() {
    clearChangeTimer();
    changeTimer = setTimeout(function () {
        updateButtonState();
        saveField("key");
    }, 600);
}
function onKey(evt) {
    // esc clears focus, allowing dialog to close
    if (evt.code === "Escape") {
        currentField.blur();
        return;
    }
    // prefer <br> instead of <div></div>
    if (evt.code === "Enter" && !inListItem()) {
        evt.preventDefault();
        document.execCommand("insertLineBreak");
        return;
    }
    // fix Ctrl+right/left handling in RTL fields
    if (currentField.dir === "rtl") {
        const selection = window.getSelection();
        let granularity = "character";
        let alter = "move";
        if (evt.ctrlKey) {
            granularity = "word";
        }
        if (evt.shiftKey) {
            alter = "extend";
        }
        if (evt.code === "ArrowRight") {
            selection.modify(alter, "right", granularity);
            evt.preventDefault();
            return;
        }
        else if (evt.code === "ArrowLeft") {
            selection.modify(alter, "left", granularity);
            evt.preventDefault();
            return;
        }
    }
    triggerKeyTimer();
}
function onKeyUp(evt) {
    // Avoid div element on remove
    if (evt.code === "Enter" || evt.code === "Backspace") {
        const anchor = window.getSelection().anchorNode;
        if (nodeIsElement(anchor) &&
            anchor.tagName === "DIV" &&
            !anchor.classList.contains("field") &&
            anchor.childElementCount === 1 &&
            anchor.children[0].tagName === "BR") {
            anchor.replaceWith(anchor.children[0]);
        }
    }
}
function nodeIsElement(node) {
    return node.nodeType === Node.ELEMENT_NODE;
}
function inListItem() {
    const anchor = window.getSelection().anchorNode;
    let n = nodeIsElement(anchor) ? anchor : anchor.parentElement;
    let inList = false;
    while (n) {
        inList = inList || window.getComputedStyle(n).display == "list-item";
        n = n.parentElement;
    }
    return inList;
}
function insertNewline() {
    if (!inPreEnvironment()) {
        setFormat("insertText", "\n");
        return;
    }
    // in some cases inserting a newline will not show any changes,
    // as a trailing newline at the end of a block does not render
    // differently. so in such cases we note the height has not
    // changed and insert an extra newline.
    const r = window.getSelection().getRangeAt(0);
    if (!r.collapsed) {
        // delete any currently selected text first, making
        // sure the delete is undoable
        setFormat("delete");
    }
    const oldHeight = currentField.clientHeight;
    setFormat("inserthtml", "\n");
    if (currentField.clientHeight === oldHeight) {
        setFormat("inserthtml", "\n");
    }
}
// is the cursor in an environment that respects whitespace?
function inPreEnvironment() {
    const anchor = window.getSelection().anchorNode;
    const n = nodeIsElement(anchor) ? anchor : anchor.parentElement;
    return window.getComputedStyle(n).whiteSpace.startsWith("pre");
}
function onInput() {
    // make sure IME changes get saved
    triggerKeyTimer();
}
function updateButtonState() {
    const buts = ["bold", "italic", "underline", "superscript", "subscript"];
    for (const name of buts) {
        const elem = document.querySelector(`#${name}`);
        elem.classList.toggle("highlighted", document.queryCommandState(name));
    }
    // fixme: forecolor
    //    'col': document.queryCommandValue("forecolor")
}
function toggleEditorButton(buttonid) {
    const button = $(buttonid)[0];
    button.classList.toggle("highlighted");
}
function setFormat(cmd, arg, nosave = false) {
    document.execCommand(cmd, false, arg);
    if (!nosave) {
        saveField("key");
        updateButtonState();
    }
}
function clearChangeTimer() {
    if (changeTimer) {
        clearTimeout(changeTimer);
        changeTimer = null;
    }
}
function onFocus(elem) {
    if (currentField === elem) {
        // anki window refocused; current element unchanged
        return;
    }
    currentField = elem;
    pycmd(`focus:${currentFieldOrdinal()}`);
    enableButtons();
    // do this twice so that there's no flicker on newer versions
    caretToEnd();
    // scroll if bottom of element off the screen
    function pos(elem) {
        let cur = 0;
        do {
            cur += elem.offsetTop;
            elem = elem.offsetParent;
        } while (elem);
        return cur;
    }
    const y = pos(elem);
    if (window.pageYOffset + window.innerHeight < y + elem.offsetHeight ||
        window.pageYOffset > y) {
        window.scroll(0, y + elem.offsetHeight - window.innerHeight);
    }
}
function focusField(n) {
    if (n === null) {
        return;
    }
    $(`#f${n}`).focus();
}
function focusIfField(x, y) {
    const elements = document.elementsFromPoint(x, y);
    for (let i = 0; i < elements.length; i++) {
        let elem = elements[i];
        if (elem.classList.contains("field")) {
            elem.focus();
            // the focus event may not fire if the window is not active, so make sure
            // the current field is set
            currentField = elem;
            return true;
        }
    }
    return false;
}
function onPaste() {
    pycmd("paste");
    window.event.preventDefault();
}
function caretToEnd() {
    const r = document.createRange();
    r.selectNodeContents(currentField);
    r.collapse(false);
    const s = document.getSelection();
    s.removeAllRanges();
    s.addRange(r);
}
function onBlur() {
    if (!currentField) {
        return;
    }
    if (document.activeElement === currentField) {
        // other widget or window focused; current field unchanged
        saveField("key");
    }
    else {
        saveField("blur");
        currentField = null;
        disableButtons();
    }
}
function saveField(type) {
    clearChangeTimer();
    if (!currentField) {
        // no field has been focused yet
        return;
    }
    // type is either 'blur' or 'key'
    pycmd(`${type}:${currentFieldOrdinal()}:${currentNoteId}:${currentField.innerHTML}`);
}
function currentFieldOrdinal() {
    return currentField.id.substring(1);
}
function wrappedExceptForWhitespace(text, front, back) {
    const match = text.match(/^(\s*)([^]*?)(\s*)$/);
    return match[1] + front + match[2] + back + match[3];
}
function preventButtonFocus() {
    for (const element of document.querySelectorAll("button.linkb")) {
        element.addEventListener("mousedown", (evt) => {
            evt.preventDefault();
        });
    }
}
function disableButtons() {
    $("button.linkb:not(.perm)").prop("disabled", true);
}
function enableButtons() {
    $("button.linkb").prop("disabled", false);
}
// disable the buttons if a field is not currently focused
function maybeDisableButtons() {
    if (!document.activeElement || document.activeElement.className !== "field") {
        disableButtons();
    }
    else {
        enableButtons();
    }
}
function wrap(front, back) {
    wrapInternal(front, back, false);
}
/* currently unused */
function wrapIntoText(front, back) {
    wrapInternal(front, back, true);
}
function wrapInternal(front, back, plainText) {
    const s = window.getSelection();
    let r = s.getRangeAt(0);
    const content = r.cloneContents();
    const span = document.createElement("span");
    span.appendChild(content);
    if (plainText) {
        const new_ = wrappedExceptForWhitespace(span.innerText, front, back);
        setFormat("inserttext", new_);
    }
    else {
        const new_ = wrappedExceptForWhitespace(span.innerHTML, front, back);
        setFormat("inserthtml", new_);
    }
    if (!span.innerHTML) {
        // run with an empty selection; move cursor back past postfix
        r = s.getRangeAt(0);
        r.setStart(r.startContainer, r.startOffset - back.length);
        r.collapse(true);
        s.removeAllRanges();
        s.addRange(r);
    }
}
function onCutOrCopy() {
    pycmd("cutOrCopy");
    return true;
}
function setFields(fields) {
    let txt = "";
    // webengine will include the variable after enter+backspace
    // if we don't convert it to a literal colour
    const color = window
        .getComputedStyle(document.documentElement)
        .getPropertyValue("--text-fg");
    for (let i = 0; i < fields.length; i++) {
        const n = fields[i][0];
        let f = fields[i][1];
        txt += `
        <tr>
            <td class=fname id="name${i}">
                <span class="fieldname">${n}</span>
            </td>
        </tr>
        <tr>
            <td width=100%>
                <div id="f${i}"
                     onkeydown="onKey(window.event);"
                     onkeyup="onKeyUp(window.event);"
                     oninput="onInput();"
                     onmouseup="onKey(window.event);"
                     onfocus="onFocus(this);"
                     onblur="onBlur();"
                     class="field clearfix"
                     onpaste="onPaste(this);"
                     oncopy="onCutOrCopy(this);"
                     oncut="onCutOrCopy(this);"
                     contentEditable
                     style="color: ${color}"
                >${f}</div>
            </td>
        </tr>`;
    }
    $("#fields").html(`<table cellpadding=0 width=100% style='table-layout: fixed;'>${txt}</table>`);
    maybeDisableButtons();
}
function setBackgrounds(cols) {
    for (let i = 0; i < cols.length; i++) {
        const element = document.querySelector(`#f${i}`);
        element.classList.toggle("dupe", cols[i] === "dupe");
    }
}
function setFonts(fonts) {
    for (let i = 0; i < fonts.length; i++) {
        const n = $(`#f${i}`);
        n.css("font-family", fonts[i][0]).css("font-size", fonts[i][1]);
        n[0].dir = fonts[i][2] ? "rtl" : "ltr";
    }
}
function setNoteId(id) {
    currentNoteId = id;
}
function showDupes() {
    $("#dupes").show();
}
function hideDupes() {
    $("#dupes").hide();
}
let pasteHTML = function (html, internal, extendedMode) {
    html = filterHTML(html, internal, extendedMode);
    if (html !== "") {
        setFormat("inserthtml", html);
    }
};
let filterHTML = function (html, internal, extendedMode) {
    // wrap it in <top> as we aren't allowed to change top level elements
    const top = document.createElement("ankitop");
    top.innerHTML = html;
    if (internal) {
        filterInternalNode(top);
    }
    else {
        filterNode(top, extendedMode);
    }
    let outHtml = top.innerHTML;
    if (!extendedMode && !internal) {
        // collapse whitespace
        outHtml = outHtml.replace(/[\n\t ]+/g, " ");
    }
    outHtml = outHtml.trim();
    //console.log(`input html: ${html}`);
    //console.log(`outpt html: ${outHtml}`);
    return outHtml;
};
let allowedTagsBasic = {};
let allowedTagsExtended = {};
let TAGS_WITHOUT_ATTRS = ["P", "DIV", "BR", "SUB", "SUP"];
for (const tag of TAGS_WITHOUT_ATTRS) {
    allowedTagsBasic[tag] = { attrs: [] };
}
TAGS_WITHOUT_ATTRS = [
    "B",
    "BLOCKQUOTE",
    "CODE",
    "DD",
    "DL",
    "DT",
    "EM",
    "H1",
    "H2",
    "H3",
    "I",
    "LI",
    "OL",
    "PRE",
    "RP",
    "RT",
    "RUBY",
    "STRONG",
    "TABLE",
    "U",
    "UL",
];
for (const tag of TAGS_WITHOUT_ATTRS) {
    allowedTagsExtended[tag] = { attrs: [] };
}
allowedTagsBasic["IMG"] = { attrs: ["SRC"] };
allowedTagsExtended["A"] = { attrs: ["HREF"] };
allowedTagsExtended["TR"] = { attrs: ["ROWSPAN"] };
allowedTagsExtended["TD"] = { attrs: ["COLSPAN", "ROWSPAN"] };
allowedTagsExtended["TH"] = { attrs: ["COLSPAN", "ROWSPAN"] };
allowedTagsExtended["FONT"] = { attrs: ["COLOR"] };
const allowedStyling = {
    color: true,
    "background-color": true,
    "font-weight": true,
    "font-style": true,
    "text-decoration-line": true,
};
let isNightMode = function () {
    return document.body.classList.contains("nightMode");
};
let filterExternalSpan = function (elem) {
    // filter out attributes
    for (const attr of [...elem.attributes]) {
        const attrName = attr.name.toUpperCase();
        if (attrName !== "STYLE") {
            elem.removeAttributeNode(attr);
        }
    }
    // filter styling
    for (const name of [...elem.style]) {
        const value = elem.style.getPropertyValue(name);
        if (!allowedStyling.hasOwnProperty(name) ||
            // google docs adds this unnecessarily
            (name === "background-color" && value === "transparent") ||
            // ignore coloured text in night mode for now
            (isNightMode() && (name === "background-color" || name === "color"))) {
            elem.style.removeProperty(name);
        }
    }
};
allowedTagsExtended["SPAN"] = filterExternalSpan;
// add basic tags to extended
Object.assign(allowedTagsExtended, allowedTagsBasic);
function isHTMLElement(elem) {
    return elem instanceof HTMLElement;
}
// filtering from another field
let filterInternalNode = function (elem) {
    if (isHTMLElement(elem)) {
        elem.style.removeProperty("background-color");
        elem.style.removeProperty("font-size");
        elem.style.removeProperty("font-family");
    }
    // recurse
    for (let i = 0; i < elem.children.length; i++) {
        const child = elem.children[i];
        filterInternalNode(child);
    }
};
// filtering from external sources
let filterNode = function (node, extendedMode) {
    if (!nodeIsElement(node)) {
        return;
    }
    // descend first, and take a copy of the child nodes as the loop will skip
    // elements due to node modifications otherwise
    for (const child of [...node.children]) {
        filterNode(child, extendedMode);
    }
    if (node.tagName === "ANKITOP") {
        return;
    }
    const tag = extendedMode
        ? allowedTagsExtended[node.tagName]
        : allowedTagsBasic[node.tagName];
    if (!tag) {
        if (!node.innerHTML || node.tagName === "TITLE") {
            node.parentNode.removeChild(node);
        }
        else {
            node.outerHTML = node.innerHTML;
        }
    }
    else {
        if (typeof tag === "function") {
            // filtering function provided
            tag(node);
        }
        else {
            // allowed, filter out attributes
            for (const attr of [...node.attributes]) {
                const attrName = attr.name.toUpperCase();
                if (tag.attrs.indexOf(attrName) === -1) {
                    node.removeAttributeNode(attr);
                }
            }
        }
    }
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZWRpdG9yLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiLi4vLi4vLi4vLi4vLi4vLi4vLi4vLi4vcXQvYXF0L2RhdGEvd2ViL2pzL2VkaXRvci50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiO0FBQUE7a0ZBQ2tGO0FBRWxGLElBQUksWUFBWSxHQUFHLElBQUksQ0FBQztBQUN4QixJQUFJLFdBQVcsR0FBRyxJQUFJLENBQUM7QUFDdkIsSUFBSSxhQUFhLEdBQUcsSUFBSSxDQUFDO0FBTXpCLHlDQUF5QztBQUN6QyxNQUFNLENBQUMsU0FBUyxDQUFDLE1BQU0sR0FBRyxVQUFVLEdBQUcsSUFBYztJQUNqRCxPQUFPLElBQUksQ0FBQyxPQUFPLENBQUMsVUFBVSxFQUFFLENBQUMsQ0FBUyxFQUFRLEVBQUU7UUFDaEQsTUFBTSxLQUFLLEdBQUcsQ0FBQyxDQUFDLEtBQUssQ0FBQyxLQUFLLENBQUMsQ0FBQztRQUU3QixPQUFPLEtBQUssQ0FBQyxDQUFDLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUM7SUFDdkMsQ0FBQyxDQUFDLENBQUM7QUFDUCxDQUFDLENBQUM7QUFFRixTQUFTLFdBQVcsQ0FBQyxHQUFXO0lBQzVCLENBQUMsQ0FBQyxZQUFZLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxLQUFLLENBQUMsZUFBZSxHQUFHLEdBQUcsQ0FBQztBQUNuRCxDQUFDO0FBRUQsU0FBUyxPQUFPLENBQUMsU0FBa0I7SUFDL0IsSUFBSSxDQUFDLFlBQVksRUFBRTtRQUNmLE9BQU87S0FDVjtJQUVELGdCQUFnQixFQUFFLENBQUM7SUFFbkIsSUFBSSxTQUFTLEVBQUU7UUFDWCxTQUFTLENBQUMsS0FBSyxDQUFDLENBQUM7S0FDcEI7U0FBTTtRQUNILCtCQUErQjtRQUMvQixZQUFZLENBQUMsSUFBSSxFQUFFLENBQUM7S0FDdkI7QUFDTCxDQUFDO0FBRUQsU0FBUyxlQUFlO0lBQ3BCLGdCQUFn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QyxJQUFJLENBQUMsbUJBQW1CLENBQUMsSUFBSSxDQUFDLENBQUM7aUJBQ2xDO2FBQ0o7U0FDSjtLQUNKO0FBQ0wsQ0FBQyxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyogQ29weXJpZ2h0OiBBbmtpdGVjdHMgUHR5IEx0ZCBhbmQgY29udHJpYnV0b3JzXG4gKiBMaWNlbnNlOiBHTlUgQUdQTCwgdmVyc2lvbiAzIG9yIGxhdGVyOyBodHRwOi8vd3d3LmdudS5vcmcvbGljZW5zZXMvYWdwbC5odG1sICovXG5cbmxldCBjdXJyZW50RmllbGQgPSBudWxsO1xubGV0IGNoYW5nZVRpbWVyID0gbnVsbDtcbmxldCBjdXJyZW50Tm90ZUlkID0gbnVsbDtcblxuZGVjbGFyZSBpbnRlcmZhY2UgU3RyaW5nIHtcbiAgICBmb3JtYXQoLi4uYXJnczogc3RyaW5nW10pOiBzdHJpbmc7XG59XG5cbi8qIGtlcHQgZm9yIGNvbXBhdGliaWxpdHkgd2l0aCBhZGQtb25zICovXG5TdHJpbmcucHJvdG90eXBlLmZvcm1hdCA9IGZ1bmN0aW9uICguLi5hcmdzOiBzdHJpbmdbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMucmVwbGFjZSgvXFx7XFxkK1xcfS9nLCAobTogc3RyaW5nKTogdm9pZCA9PiB7XG4gICAgICAgIGNvbnN0IG1hdGNoID0gbS5tYXRjaCgvXFxkKy8pO1xuXG4gICAgICAgIHJldHVybiBtYXRjaCA/IGFyZ3NbbWF0Y2hbMF1dIDogXCJcIjtcbiAgICB9KTtcbn07XG5cbmZ1bmN0aW9uIHNldEZHQnV0dG9uKGNvbDogc3RyaW5nKTogdm9pZCB7XG4gICAgJChcIiNmb3JlY29sb3JcIilbMF0uc3R5bGUuYmFja2dyb3VuZENvbG9yID0gY29sO1xufVxuXG5mdW5jdGlvbiBzYXZlTm93KGtlZXBGb2N1czogYm9vbGVhbik6IHZvaWQge1xuICAgIGlmICghY3VycmVudEZpZWxkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjbGVhckNoYW5nZVRpbWVyKCk7XG5cbiAgICBpZiAoa2VlcEZvY3VzKSB7XG4gICAgICAgIHNhdmVGaWVsZChcImtleVwiKTtcbiAgICB9IGVsc2Uge1xuICAgICAgICAvLyB0cmlnZ2VycyBvbkJsdXIsIHdoaWNoIHNhdmVzXG4gICAgICAgIGN1cnJlbnRGaWVsZC5ibHVyKCk7XG4gICAgfVxufVxuXG5mdW5jdGlvbiB0cmlnZ2VyS2V5VGltZXIoKTogdm9pZCB7XG4gICAgY2xlYXJDaGFuZ2VUaW1lcigpO1xuICAgIGNoYW5nZVRpbWVyID0gc2V0VGltZW91dChmdW5jdGlvbiAoKSB7XG4gICAgICAgIHVwZGF0ZUJ1dHRvblN0YXRlKCk7XG4gICAgICAgIHNhdmVGaWVsZChcImtleVwiKTtcbiAgICB9LCA2MDApO1xufVxuXG5pbnRlcmZhY2UgU2VsZWN0aW9uIHtcbiAgICBtb2RpZnkoczogc3RyaW5nLCB0OiBzdHJpbmcsIHU6IHN0cmluZyk6IHZvaWQ7XG59XG5cbmZ1bmN0aW9uIG9uS2V5KGV2dDogS2V5Ym9hcmRFdmVudCk6IHZvaWQge1xuICAgIC8vIGVzYyBjbGVhcnMgZm9jdXMsIGFsbG93aW5nIGRpYWxvZyB0byBjbG9zZVxuICAgIGlmIChldnQuY29kZSA9PT0gXCJFc2NhcGVcIikge1xuICAgICAgICBjdXJyZW50RmllbGQuYmx1cigpO1xuICAgICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gcHJlZmVyIDxicj4gaW5zdGVhZCBvZiA8ZGl2PjwvZGl2PlxuICAgIGlmIChldnQuY29kZSA9PT0gXCJFbnRlclwiICYmICFpbkxpc3RJdGVtKCkpIHtcbiAgICAgICAgZXZ0LnByZXZlbnREZWZhdWx0KCk7XG4gICAgICAgIGRvY3VtZW50LmV4ZWNDb21tYW5kKFwiaW5zZXJ0TGluZUJyZWFrXCIpO1xuICAgICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gZml4IEN0cmwrcmlnaHQvbGVmdCBoYW5kbGluZyBpbiBSVEwgZmllbGRzXG4gICAgaWYgKGN1cnJlbnRGaWVsZC5kaXIgPT09IFwicnRsXCIpIHtcbiAgICAgICAgY29uc3Qgc2VsZWN0aW9uID0gd2luZG93LmdldFNlbGVjdGlvbigpO1xuICAgICAgICBsZXQgZ3JhbnVsYXJpdHkgPSBcImNoYXJhY3RlclwiO1xuICAgICAgICBsZXQgYWx0ZXIgPSBcIm1vdmVcIjtcbiAgICAgICAgaWYgKGV2dC5jdHJsS2V5KSB7XG4gICAgICAgICAgICBncmFudWxhcml0eSA9IFwid29yZFwiO1xuICAgICAgICB9XG4gICAgICAgIGlmIChldnQuc2hpZnRLZXkpIHtcbiAgICAgICAgICAgIGFsdGVyID0gXCJleHRlbmRcIjtcbiAgICAgICAgfVxuICAgICAgICBpZiAoZXZ0LmNvZGUgPT09IFwiQXJyb3dSaWdodFwiKSB7XG4gICAgICAgICAgICBzZWxlY3Rpb24ubW9kaWZ5KGFsdGVyLCBcInJpZ2h0XCIsIGdyYW51bGFyaXR5KTtcbiAgICAgICAgICAgIGV2dC5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9IGVsc2UgaWYgKGV2dC5jb2RlID09PSBcIkFycm93TGVmdFwiKSB7XG4gICAgICAgICAgICBzZWxlY3Rpb24ubW9kaWZ5KGFsdGVyLCBcImxlZnRcIiwgZ3JhbnVsYXJpdHkpO1xuICAgICAgICAgICAgZXZ0LnByZXZlbnREZWZhdWx0KCk7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICB0cmlnZ2VyS2V5VGltZXIoKTtcbn1cblxuZnVuY3Rpb24gb25LZXlVcChldnQ6IEtleWJvYXJkRXZlbnQpOiB2b2lkIHtcbiAgICAvLyBBdm9pZCBkaXYgZWxlbWVudCBvbiByZW1vdmVcbiAgICBpZiAoZXZ0LmNvZGUgPT09IFwiRW50ZXJcIiB8fCBldnQuY29kZSA9PT0gXCJCYWNrc3BhY2VcIikge1xuICAgICAgICBjb25zdCBhbmNob3IgPSB3aW5kb3cuZ2V0U2VsZWN0aW9uKCkuYW5jaG9yTm9kZTtcblxuICAgICAgICBpZiAoXG4gICAgICAgICAgICBub2RlSXNFbGVtZW50KGFuY2hvcikgJiZcbiAgICAgICAgICAgIGFuY2hvci50YWdOYW1lID09PSBcIkRJVlwiICYmXG4gICAgICAgICAgICAhYW5jaG9yLmNsYXNzTGlzdC5jb250YWlucyhcImZpZWxkXCIpICYmXG4gICAgICAgICAgICBhbmNob3IuY2hpbGRFbGVtZW50Q291bnQgPT09IDEgJiZcbiAgICAgICAgICAgIGFuY2hvci5jaGlsZHJlblswXS50YWdOYW1lID09PSBcIkJSXCJcbiAgICAgICAgKSB7XG4gICAgICAgICAgICBhbmNob3IucmVwbGFjZVdpdGgoYW5jaG9yLmNoaWxkcmVuWzBdKTtcbiAgICAgICAgfVxuICAgIH1cbn1cblxuZnVuY3Rpb24gbm9kZUlzRWxlbWVudChub2RlOiBOb2RlKTogbm9kZSBpcyBFbGVtZW50IHtcbiAgICByZXR1cm4gbm9kZS5ub2RlVHlwZSA9PT0gTm9kZS5FTEVNRU5UX05PREU7XG59XG5cbmZ1bmN0aW9uIGluTGlzdEl0ZW0oKTogYm9vbGVhbiB7XG4gICAgY29uc3QgYW5jaG9yID0gd2luZG93LmdldFNlbGVjdGlvbigpLmFuY2hvck5vZGU7XG5cbiAgICBsZXQgbiA9IG5vZGVJc0VsZW1lbnQoYW5jaG9yKSA/IGFuY2hvciA6IGFuY2hvci5wYXJlbnRFbGVtZW50O1xuXG4gICAgbGV0IGluTGlzdCA9IGZhbHNlO1xuXG4gICAgd2hpbGUgKG4pIHtcbiAgICAgICAgaW5MaXN0ID0gaW5MaXN0IHx8IHdpbmRvdy5nZXRDb21wdXRlZFN0eWxlKG4pLmRpc3BsYXkgPT0gXCJsaXN0LWl0ZW1cIjtcbiAgICAgICAgbiA9IG4ucGFyZW50RWxlbWVudDtcbiAgICB9XG5cbiAgICByZXR1cm4gaW5MaXN0O1xufVxuXG5mdW5jdGlvbiBpbnNlcnROZXdsaW5lKCk6IHZvaWQge1xuICAgIGlmICghaW5QcmVFbnZpcm9ubWVudCgpKSB7XG4gICAgICAgIHNldEZvcm1hdChcImluc2VydFRleHRcIiwgXCJcXG5cIik7XG4gICAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBpbiBzb21lIGNhc2VzIGluc2VydGluZyBhIG5ld2xpbmUgd2lsbCBub3Qgc2hvdyBhbnkgY2hhbmdlcyxcbiAgICAvLyBhcyBhIHRyYWlsaW5nIG5ld2xpbmUgYXQgdGhlIGVuZCBvZiBhIGJsb2NrIGRvZXMgbm90IHJlbmRlclxuICAgIC8vIGRpZmZlcmVudGx5LiBzbyBpbiBzdWNoIGNhc2VzIHdlIG5vdGUgdGhlIGhlaWdodCBoYXMgbm90XG4gICAgLy8gY2hhbmdlZCBhbmQgaW5zZXJ0IGFuIGV4dHJhIG5ld2xpbmUuXG5cbiAgICBjb25zdCByID0gd2luZG93LmdldFNlbGVjdGlvbigpLmdldFJhbmdlQXQoMCk7XG4gICAgaWYgKCFyLmNvbGxhcHNlZCkge1xuICAgICAgICAvLyBkZWxldGUgYW55IGN1cnJlbnRseSBzZWxlY3RlZCB0ZXh0IGZpcnN0LCBtYWtpbmdcbiAgICAgICAgLy8gc3VyZSB0aGUgZGVsZXRlIGlzIHVuZG9hYmxlXG4gICAgICAgIHNldEZvcm1hdChcImRlbGV0ZVwiKTtcbiAgICB9XG5cbiAgICBjb25zdCBvbGRIZWlnaHQgPSBjdXJyZW50RmllbGQuY2xpZW50SGVpZ2h0O1xuICAgIHNldEZvcm1hdChcImluc2VydGh0bWxcIiwgXCJcXG5cIik7XG4gICAgaWYgKGN1cnJlbnRGaWVsZC5jbGllbnRIZWlnaHQgPT09IG9sZEhlaWdodCkge1xuICAgICAgICBzZXRGb3JtYXQoXCJpbnNlcnRodG1sXCIsIFwiXFxuXCIpO1xuICAgIH1cbn1cblxuLy8gaXMgdGhlIGN1cnNvciBpbiBhbiBlbnZpcm9ubWVudCB0aGF0IHJlc3BlY3RzIHdoaXRlc3BhY2U/XG5mdW5jdGlvbiBpblByZUVudmlyb25tZW50KCk6IGJvb2xlYW4ge1xuICAgIGNvbnN0IGFuY2hvciA9IHdpbmRvdy5nZXRTZWxlY3Rpb24oKS5hbmNob3JOb2RlO1xuICAgIGNvbnN0IG4gPSBub2RlSXNFbGVtZW50KGFuY2hvcikgPyBhbmNob3IgOiBhbmNob3IucGFyZW50RWxlbWVudDtcblxuICAgIHJldHVybiB3aW5kb3cuZ2V0Q29tcHV0ZWRTdHlsZShuKS53aGl0ZVNwYWNlLnN0YXJ0c1dpdGgoXCJwcmVcIik7XG59XG5cbmZ1bmN0aW9uIG9uSW5wdXQoKTogdm9pZCB7XG4gICAgLy8gbWFrZSBzdXJlIElNRSBjaGFuZ2VzIGdldCBzYXZlZFxuICAgIHRyaWdnZXJLZXlUaW1lcigpO1xufVxuXG5mdW5jdGlvbiB1cGRhdGVCdXR0b25TdGF0ZSgpOiB2b2lkIHtcbiAgICBjb25zdCBidXRzID0gW1wiYm9sZFwiLCBcIml0YWxpY1wiLCBcInVuZGVybGluZVwiLCBcInN1cGVyc2NyaXB0XCIsIFwic3Vic2NyaXB0XCJdO1xuICAgIGZvciAoY29uc3QgbmFtZSBvZiBidXRzKSB7XG4gICAgICAgIGNvbnN0IGVsZW0gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKGAjJHtuYW1lfWApIGFzIEhUTUxFbGVtZW50O1xuICAgICAgICBlbGVtLmNsYXNzTGlzdC50b2dnbGUoXCJoaWdobGlnaHRlZFwiLCBkb2N1bWVudC5xdWVyeUNvbW1hbmRTdGF0ZShuYW1lKSk7XG4gICAgfVxuXG4gICAgLy8gZml4bWU6IGZvcmVjb2xvclxuICAgIC8vICAgICdjb2wnOiBkb2N1bWVudC5xdWVyeUNvbW1hbmRWYWx1ZShcImZvcmVjb2xvclwiKVxufVxuXG5mdW5jdGlvbiB0b2dnbGVFZGl0b3JCdXR0b24oYnV0dG9uaWQ6IHN0cmluZyk6IHZvaWQge1xuICAgIGNvbnN0IGJ1dHRvbiA9ICQoYnV0dG9uaWQpWzBdO1xuICAgIGJ1dHRvbi5jbGFzc0xpc3QudG9nZ2xlKFwiaGlnaGxpZ2h0ZWRcIik7XG59XG5cbmZ1bmN0aW9uIHNldEZvcm1hdChjbWQ6IHN0cmluZywgYXJnPzogYW55LCBub3NhdmU6IGJvb2xlYW4gPSBmYWxzZSk6IHZvaWQge1xuICAgIGRvY3VtZW50LmV4ZWNDb21tYW5kKGNtZCwgZmFsc2UsIGFyZyk7XG4gICAgaWYgKCFub3NhdmUpIHtcbiAgICAgICAgc2F2ZUZpZWxkKFwia2V5XCIpO1xuICAgICAgICB1cGRhdGVCdXR0b25TdGF0ZSgpO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gY2xlYXJDaGFuZ2VUaW1lcigpOiB2b2lkIHtcbiAgICBpZiAoY2hhbmdlVGltZXIpIHtcbiAgICAgICAgY2xlYXJUaW1lb3V0KGNoYW5nZVRpbWVyKTtcbiAgICAgICAgY2hhbmdlVGltZXIgPSBudWxsO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gb25Gb2N1cyhlbGVtOiBIVE1MRWxlbWVudCk6IHZvaWQge1xuICAgIGlmIChjdXJyZW50RmllbGQgPT09IGVsZW0pIHtcbiAgICAgICAgLy8gYW5raSB3aW5kb3cgcmVmb2N1c2VkOyBjdXJyZW50IGVsZW1lbnQgdW5jaGFuZ2VkXG4gICAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY3VycmVudEZpZWxkID0gZWxlbTtcbiAgICBweWNtZChgZm9jdXM6JHtjdXJyZW50RmllbGRPcmRpbmFsKCl9YCk7XG4gICAgZW5hYmxlQnV0dG9ucygpO1xuICAgIC8vIGRvIHRoaXMgdHdpY2Ugc28gdGhhdCB0aGVyZSdzIG5vIGZsaWNrZXIgb24gbmV3ZXIgdmVyc2lvbnNcbiAgICBjYXJldFRvRW5kKCk7XG4gICAgLy8gc2Nyb2xsIGlmIGJvdHRvbSBvZiBlbGVtZW50IG9mZiB0aGUgc2NyZWVuXG4gICAgZnVuY3Rpb24gcG9zKGVsZW06IEhUTUxFbGVtZW50KTogbnVtYmVyIHtcbiAgICAgICAgbGV0IGN1ciA9IDA7XG4gICAgICAgIGRvIHtcbiAgICAgICAgICAgIGN1ciArPSBlbGVtLm9mZnNldFRvcDtcbiAgICAgICAgICAgIGVsZW0gPSBlbGVtLm9mZnNldFBhcmVudCBhcyBIVE1MRWxlbWVudDtcbiAgICAgICAgfSB3aGlsZSAoZWxlbSk7XG4gICAgICAgIHJldHVybiBjdXI7XG4gICAgfVxuXG4gICAgY29uc3QgeSA9IHBvcyhlbGVtKTtcbiAgICBpZiAoXG4gICAgICAgIHdpbmRvdy5wYWdlWU9mZnNldCArIHdpbmRvdy5pbm5lckhlaWdodCA8IHkgKyBlbGVtLm9mZnNldEhlaWdodCB8fFxuICAgICAgICB3aW5kb3cucGFnZVlPZmZzZXQgPiB5XG4gICAgKSB7XG4gICAgICAgIHdpbmRvdy5zY3JvbGwoMCwgeSArIGVsZW0ub2Zmc2V0SGVpZ2h0IC0gd2luZG93LmlubmVySGVpZ2h0KTtcbiAgICB9XG59XG5cbmZ1bmN0aW9uIGZvY3VzRmllbGQobjogbnVtYmVyKTogdm9pZCB7XG4gICAgaWYgKG4gPT09IG51bGwpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICAkKGAjZiR7bn1gKS5mb2N1cygpO1xufVxuXG5mdW5jdGlvbiBmb2N1c0lmRmllbGQoeDogbnVtYmVyLCB5OiBudW1iZXIpOiBib29sZWFuIHtcbiAgICBjb25zdCBlbGVtZW50cyA9IGRvY3VtZW50LmVsZW1lbnRzRnJvbVBvaW50KHgsIHkpO1xuICAgIGZvciAobGV0IGkgPSAwOyBpIDwgZWxlbWVudHMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgbGV0IGVsZW0gPSBlbGVtZW50c1tpXSBhcyBIVE1MRWxlbWVudDtcbiAgICAgICAgaWYgKGVsZW0uY2xhc3NMaXN0LmNvbnRhaW5zKFwiZmllbGRcIikpIHtcbiAgICAgICAgICAgIGVsZW0uZm9jdXMoKTtcbiAgICAgICAgICAgIC8vIHRoZSBmb2N1cyBldmVudCBtYXkgbm90IGZpcmUgaWYgdGhlIHdpbmRvdyBpcyBub3QgYWN0aXZlLCBzbyBtYWtlIHN1cmVcbiAgICAgICAgICAgIC8vIHRoZSBjdXJyZW50IGZpZWxkIGlzIHNldFxuICAgICAgICAgICAgY3VycmVudEZpZWxkID0gZWxlbTtcbiAgICAgICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgICB9XG4gICAgfVxuICAgIHJldHVybiBmYWxzZTtcbn1cblxuZnVuY3Rpb24gb25QYXN0ZSgpOiB2b2lkIHtcbiAgICBweWNtZChcInBhc3RlXCIpO1xuICAgIHdpbmRvdy5ldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xufVxuXG5mdW5jdGlvbiBjYXJldFRvRW5kKCk6IHZvaWQge1xuICAgIGNvbnN0IHIgPSBkb2N1bWVudC5jcmVhdGVSYW5nZSgpO1xuICAgIHIuc2VsZWN0Tm9kZUNvbnRlbnRzKGN1cnJlbnRGaWVsZCk7XG4gICAgci5jb2xsYXBzZShmYWxzZSk7XG4gICAgY29uc3QgcyA9IGRvY3VtZW50LmdldFNlbGVjdGlvbigpO1xuICAgIHMucmVtb3ZlQWxsUmFuZ2VzKCk7XG4gICAgcy5hZGRSYW5nZShyKTtcbn1cblxuZnVuY3Rpb24gb25CbHVyKCk6IHZvaWQge1xuICAgIGlmICghY3VycmVudEZpZWxkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBpZiAoZG9jdW1lbnQuYWN0aXZlRWxlbWVudCA9PT0gY3VycmVudEZpZWxkKSB7XG4gICAgICAgIC8vIG90aGVyIHdpZGdldCBvciB3aW5kb3cgZm9jdXNlZDsgY3VycmVudCBmaWVsZCB1bmNoYW5nZWRcbiAgICAgICAgc2F2ZUZpZWxkKFwia2V5XCIpO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIHNhdmVGaWVsZChcImJsdXJcIik7XG4gICAgICAgIGN1cnJlbnRGaWVsZCA9IG51bGw7XG4gICAgICAgIGRpc2FibGVCdXR0b25zKCk7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBzYXZlRmllbGQodHlwZTogXCJibHVyXCIgfCBcImtleVwiKTogdm9pZCB7XG4gICAgY2xlYXJDaGFuZ2VUaW1lcigpO1xuICAgIGlmICghY3VycmVudEZpZWxkKSB7XG4gICAgICAgIC8vIG5vIGZpZWxkIGhhcyBiZWVuIGZvY3VzZWQgeWV0XG4gICAgICAgIHJldHVybjtcbiAgICB9XG4gICAgLy8gdHlwZSBpcyBlaXRoZXIgJ2JsdXInIG9yICdrZXknXG4gICAgcHljbWQoXG4gICAgICAgIGAke3R5cGV9OiR7Y3VycmVudEZpZWxkT3JkaW5hbCgpfToke2N1cnJlbnROb3RlSWR9OiR7Y3VycmVudEZpZWxkLmlubmVySFRNTH1gXG4gICAgKTtcbn1cblxuZnVuY3Rpb24gY3VycmVudEZpZWxkT3JkaW5hbCgpOiBzdHJpbmcge1xuICAgIHJldHVybiBjdXJyZW50RmllbGQuaWQuc3Vic3RyaW5nKDEpO1xufVxuXG5mdW5jdGlvbiB3cmFwcGVkRXhjZXB0Rm9yV2hpdGVzcGFjZSh0ZXh0OiBzdHJpbmcsIGZyb250OiBzdHJpbmcsIGJhY2s6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgY29uc3QgbWF0Y2ggPSB0ZXh0Lm1hdGNoKC9eKFxccyopKFteXSo/KShcXHMqKSQvKTtcbiAgICByZXR1cm4gbWF0Y2hbMV0gKyBmcm9udCArIG1hdGNoWzJdICsgYmFjayArIG1hdGNoWzNdO1xufVxuXG5mdW5jdGlvbiBwcmV2ZW50QnV0dG9uRm9jdXMoKTogdm9pZCB7XG4gICAgZm9yIChjb25zdCBlbGVtZW50IG9mIGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoXCJidXR0b24ubGlua2JcIikpIHtcbiAgICAgICAgZWxlbWVudC5hZGRFdmVudExpc3RlbmVyKFwibW91c2Vkb3duXCIsIChldnQ6IEV2ZW50KSA9PiB7XG4gICAgICAgICAgICBldnQucHJldmVudERlZmF1bHQoKTtcbiAgICAgICAgfSk7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBkaXNhYmxlQnV0dG9ucygpOiB2b2lkIHtcbiAgICAkKFwiYnV0dG9uLmxpbmtiOm5vdCgucGVybSlcIikucHJvcChcImRpc2FibGVkXCIsIHRydWUpO1xufVxuXG5mdW5jdGlvbiBlbmFibGVCdXR0b25zKCk6IHZvaWQge1xuICAgICQoXCJidXR0b24ubGlua2JcIikucHJvcChcImRpc2FibGVkXCIsIGZhbHNlKTtcbn1cblxuLy8gZGlzYWJsZSB0aGUgYnV0dG9ucyBpZiBhIGZpZWxkIGlzIG5vdCBjdXJyZW50bHkgZm9jdXNlZFxuZnVuY3Rpb24gbWF5YmVEaXNhYmxlQnV0dG9ucygpOiB2b2lkIHtcbiAgICBpZiAoIWRvY3VtZW50LmFjdGl2ZUVsZW1lbnQgfHwgZG9jdW1lbnQuYWN0aXZlRWxlbWVudC5jbGFzc05hbWUgIT09IFwiZmllbGRcIikge1xuICAgICAgICBkaXNhYmxlQnV0dG9ucygpO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIGVuYWJsZUJ1dHRvbnMoKTtcbiAgICB9XG59XG5cbmZ1bmN0aW9uIHdyYXAoZnJvbnQ6IHN0cmluZywgYmFjazogc3RyaW5nKTogdm9pZCB7XG4gICAgd3JhcEludGVybmFsKGZyb250LCBiYWNrLCBmYWxzZSk7XG59XG5cbi8qIGN1cnJlbnRseSB1bnVzZWQgKi9cbmZ1bmN0aW9uIHdyYXBJbnRvVGV4dChmcm9udDogc3RyaW5nLCBiYWNrOiBzdHJpbmcpOiB2b2lkIHtcbiAgICB3cmFwSW50ZXJuYWwoZnJvbnQsIGJhY2ssIHRydWUpO1xufVxuXG5mdW5jdGlvbiB3cmFwSW50ZXJuYWwoZnJvbnQ6IHN0cmluZywgYmFjazogc3RyaW5nLCBwbGFpblRleHQ6IGJvb2xlYW4pOiB2b2lkIHtcbiAgICBjb25zdCBzID0gd2luZG93LmdldFNlbGVjdGlvbigpO1xuICAgIGxldCByID0gcy5nZXRSYW5nZUF0KDApO1xuICAgIGNvbnN0IGNvbnRlbnQgPSByLmNsb25lQ29udGVudHMoKTtcbiAgICBjb25zdCBzcGFuID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcInNwYW5cIik7XG4gICAgc3Bhbi5hcHBlbmRDaGlsZChjb250ZW50KTtcbiAgICBpZiAocGxhaW5UZXh0KSB7XG4gICAgICAgIGNvbnN0IG5ld18gPSB3cmFwcGVkRXhjZXB0Rm9yV2hpdGVzcGFjZShzcGFuLmlubmVyVGV4dCwgZnJvbnQsIGJhY2spO1xuICAgICAgICBzZXRGb3JtYXQoXCJpbnNlcnR0ZXh0XCIsIG5ld18pO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIGNvbnN0IG5ld18gPSB3cmFwcGVkRXhjZXB0Rm9yV2hpdGVzcGFjZShzcGFuLmlubmVySFRNTCwgZnJvbnQsIGJhY2spO1xuICAgICAgICBzZXRGb3JtYXQoXCJpbnNlcnRodG1sXCIsIG5ld18pO1xuICAgIH1cbiAgICBpZiAoIXNwYW4uaW5uZXJIVE1MKSB7XG4gICAgICAgIC8vIHJ1biB3aXRoIGFuIGVtcHR5IHNlbGVjdGlvbjsgbW92ZSBjdXJzb3IgYmFjayBwYXN0IHBvc3RmaXhcbiAgICAgICAgciA9IHMuZ2V0UmFuZ2VBdCgwKTtcbiAgICAgICAgci5zZXRTdGFydChyLnN0YXJ0Q29udGFpbmVyLCByLnN0YXJ0T2Zmc2V0IC0gYmFjay5sZW5ndGgpO1xuICAgICAgICByLmNvbGxhcHNlKHRydWUpO1xuICAgICAgICBzLnJlbW92ZUFsbFJhbmdlcygpO1xuICAgICAgICBzLmFkZFJhbmdlKHIpO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gb25DdXRPckNvcHkoKTogYm9vbGVhbiB7XG4gICAgcHljbWQoXCJjdXRPckNvcHlcIik7XG4gICAgcmV0dXJuIHRydWU7XG59XG5cbmZ1bmN0aW9uIHNldEZpZWxkcyhmaWVsZHM6IFtzdHJpbmcsIHN0cmluZ11bXSk6IHZvaWQge1xuICAgIGxldCB0eHQgPSBcIlwiO1xuICAgIC8vIHdlYmVuZ2luZSB3aWxsIGluY2x1ZGUgdGhlIHZhcmlhYmxlIGFmdGVyIGVudGVyK2JhY2tzcGFjZVxuICAgIC8vIGlmIHdlIGRvbid0IGNvbnZlcnQgaXQgdG8gYSBsaXRlcmFsIGNvbG91clxuICAgIGNvbnN0IGNvbG9yID0gd2luZG93XG4gICAgICAgIC5nZXRDb21wdXRlZFN0eWxlKGRvY3VtZW50LmRvY3VtZW50RWxlbWVudClcbiAgICAgICAgLmdldFByb3BlcnR5VmFsdWUoXCItLXRleHQtZmdcIik7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBmaWVsZHMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgY29uc3QgbiA9IGZpZWxkc1tpXVswXTtcbiAgICAgICAgbGV0IGYgPSBmaWVsZHNbaV1bMV07XG4gICAgICAgIHR4dCArPSBgXG4gICAgICAgIDx0cj5cbiAgICAgICAgICAgIDx0ZCBjbGFzcz1mbmFtZSBpZD1cIm5hbWUke2l9XCI+XG4gICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9XCJmaWVsZG5hbWVcIj4ke259PC9zcGFuPlxuICAgICAgICAgICAgPC90ZD5cbiAgICAgICAgPC90cj5cbiAgICAgICAgPHRyPlxuICAgICAgICAgICAgPHRkIHdpZHRoPTEwMCU+XG4gICAgICAgICAgICAgICAgPGRpdiBpZD1cImYke2l9XCJcbiAgICAgICAgICAgICAgICAgICAgIG9ua2V5ZG93bj1cIm9uS2V5KHdpbmRvdy5ldmVudCk7XCJcbiAgICAgICAgICAgICAgICAgICAgIG9ua2V5dXA9XCJvbktleVVwKHdpbmRvdy5ldmVudCk7XCJcbiAgICAgICAgICAgICAgICAgICAgIG9uaW5wdXQ9XCJvbklucHV0KCk7XCJcbiAgICAgICAgICAgICAgICAgICAgIG9ubW91c2V1cD1cIm9uS2V5KHdpbmRvdy5ldmVudCk7XCJcbiAgICAgICAgICAgICAgICAgICAgIG9uZm9jdXM9XCJvbkZvY3VzKHRoaXMpO1wiXG4gICAgICAgICAgICAgICAgICAgICBvbmJsdXI9XCJvbkJsdXIoKTtcIlxuICAgICAgICAgICAgICAgICAgICAgY2xhc3M9XCJmaWVsZCBjbGVhcmZpeFwiXG4gICAgICAgICAgICAgICAgICAgICBvbnBhc3RlPVwib25QYXN0ZSh0aGlzKTtcIlxuICAgICAgICAgICAgICAgICAgICAgb25jb3B5PVwib25DdXRPckNvcHkodGhpcyk7XCJcbiAgICAgICAgICAgICAgICAgICAgIG9uY3V0PVwib25DdXRPckNvcHkodGhpcyk7XCJcbiAgICAgICAgICAgICAgICAgICAgIGNvbnRlbnRFZGl0YWJsZVxuICAgICAgICAgICAgICAgICAgICAgc3R5bGU9XCJjb2xvcjogJHtjb2xvcn1cIlxuICAgICAgICAgICAgICAgID4ke2Z9PC9kaXY+XG4gICAgICAgICAgICA8L3RkPlxuICAgICAgICA8L3RyPmA7XG4gICAgfVxuICAgICQoXCIjZmllbGRzXCIpLmh0bWwoXG4gICAgICAgIGA8dGFibGUgY2VsbHBhZGRpbmc9MCB3aWR0aD0xMDAlIHN0eWxlPSd0YWJsZS1sYXlvdXQ6IGZpeGVkOyc+JHt0eHR9PC90YWJsZT5gXG4gICAgKTtcbiAgICBtYXliZURpc2FibGVCdXR0b25zKCk7XG59XG5cbmZ1bmN0aW9uIHNldEJhY2tncm91bmRzKGNvbHM6IFwiZHVwZVwiW10pIHtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IGNvbHMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgY29uc3QgZWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoYCNmJHtpfWApO1xuICAgICAgICBlbGVtZW50LmNsYXNzTGlzdC50b2dnbGUoXCJkdXBlXCIsIGNvbHNbaV0gPT09IFwiZHVwZVwiKTtcbiAgICB9XG59XG5cbmZ1bmN0aW9uIHNldEZvbnRzKGZvbnRzOiBbc3RyaW5nLCBudW1iZXIsIGJvb2xlYW5dW10pOiB2b2lkIHtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IGZvbnRzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgIGNvbnN0IG4gPSAkKGAjZiR7aX1gKTtcbiAgICAgICAgbi5jc3MoXCJmb250LWZhbWlseVwiLCBmb250c1tpXVswXSkuY3NzKFwiZm9udC1zaXplXCIsIGZvbnRzW2ldWzFdKTtcbiAgICAgICAgblswXS5kaXIgPSBmb250c1tpXVsyXSA/IFwicnRsXCIgOiBcImx0clwiO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gc2V0Tm90ZUlkKGlkOiBudW1iZXIpOiB2b2lkIHtcbiAgICBjdXJyZW50Tm90ZUlkID0gaWQ7XG59XG5cbmZ1bmN0aW9uIHNob3dEdXBlcygpOiB2b2lkIHtcbiAgICAkKFwiI2R1cGVzXCIpLnNob3coKTtcbn1cblxuZnVuY3Rpb24gaGlkZUR1cGVzKCk6IHZvaWQge1xuICAgICQoXCIjZHVwZXNcIikuaGlkZSgpO1xufVxuXG5sZXQgcGFzdGVIVE1MID0gZnVuY3Rpb24gKFxuICAgIGh0bWw6IHN0cmluZyxcbiAgICBpbnRlcm5hbDogYm9vbGVhbixcbiAgICBleHRlbmRlZE1vZGU6IGJvb2xlYW5cbik6IHZvaWQge1xuICAgIGh0bWwgPSBmaWx0ZXJIVE1MKGh0bWwsIGludGVybmFsLCBleHRlbmRlZE1vZGUpO1xuXG4gICAgaWYgKGh0bWwgIT09IFwiXCIpIHtcbiAgICAgICAgc2V0Rm9ybWF0KFwiaW5zZXJ0aHRtbFwiLCBodG1sKTtcbiAgICB9XG59O1xuXG5sZXQgZmlsdGVySFRNTCA9IGZ1bmN0aW9uIChcbiAgICBodG1sOiBzdHJpbmcsXG4gICAgaW50ZXJuYWw6IGJvb2xlYW4sXG4gICAgZXh0ZW5kZWRNb2RlOiBib29sZWFuXG4pOiBzdHJpbmcge1xuICAgIC8vIHdyYXAgaXQgaW4gPHRvcD4gYXMgd2UgYXJlbid0IGFsbG93ZWQgdG8gY2hhbmdlIHRvcCBsZXZlbCBlbGVtZW50c1xuICAgIGNvbnN0IHRvcCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJhbmtpdG9wXCIpO1xuICAgIHRvcC5pbm5lckhUTUwgPSBodG1sO1xuXG4gICAgaWYgKGludGVybmFsKSB7XG4gICAgICAgIGZpbHRlckludGVybmFsTm9kZSh0b3ApO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIGZpbHRlck5vZGUodG9wLCBleHRlbmRlZE1vZGUpO1xuICAgIH1cbiAgICBsZXQgb3V0SHRtbCA9IHRvcC5pbm5lckhUTUw7XG4gICAgaWYgKCFleHRlbmRlZE1vZGUgJiYgIWludGVybmFsKSB7XG4gICAgICAgIC8vIGNvbGxhcHNlIHdoaXRlc3BhY2VcbiAgICAgICAgb3V0SHRtbCA9IG91dEh0bWwucmVwbGFjZSgvW1xcblxcdCBdKy9nLCBcIiBcIik7XG4gICAgfVxuICAgIG91dEh0bWwgPSBvdXRIdG1sLnRyaW0oKTtcbiAgICAvL2NvbnNvbGUubG9nKGBpbnB1dCBodG1sOiAke2h0bWx9YCk7XG4gICAgLy9jb25zb2xlLmxvZyhgb3V0cHQgaHRtbDogJHtvdXRIdG1sfWApO1xuICAgIHJldHVybiBvdXRIdG1sO1xufTtcblxubGV0IGFsbG93ZWRUYWdzQmFzaWMgPSB7fTtcbmxldCBhbGxvd2VkVGFnc0V4dGVuZGVkID0ge307XG5cbmxldCBUQUdTX1dJVEhPVVRfQVRUUlMgPSBbXCJQXCIsIFwiRElWXCIsIFwiQlJcIiwgXCJTVUJcIiwgXCJTVVBcIl07XG5mb3IgKGNvbnN0IHRhZyBvZiBUQUdTX1dJVEhPVVRfQVRUUlMpIHtcbiAgICBhbGxvd2VkVGFnc0Jhc2ljW3RhZ10gPSB7IGF0dHJzOiBbXSB9O1xufVxuXG5UQUdTX1dJVEhPVVRfQVRUUlMgPSBbXG4gICAgXCJCXCIsXG4gICAgXCJCTE9DS1FVT1RFXCIsXG4gICAgXCJDT0RFXCIsXG4gICAgXCJERFwiLFxuICAgIFwiRExcIixcbiAgICBcIkRUXCIsXG4gICAgXCJFTVwiLFxuICAgIFwiSDFcIixcbiAgICBcIkgyXCIsXG4gICAgXCJIM1wiLFxuICAgIFwiSVwiLFxuICAgIFwiTElcIixcbiAgICBcIk9MXCIsXG4gICAgXCJQUkVcIixcbiAgICBcIlJQXCIsXG4gICAgXCJSVFwiLFxuICAgIFwiUlVCWVwiLFxuICAgIFwiU1RST05HXCIsXG4gICAgXCJUQUJMRVwiLFxuICAgIFwiVVwiLFxuICAgIFwiVUxcIixcbl07XG5mb3IgKGNvbnN0IHRhZyBvZiBUQUdTX1dJVEhPVVRfQVRUUlMpIHtcbiAgICBhbGxvd2VkVGFnc0V4dGVuZGVkW3RhZ10gPSB7IGF0dHJzOiBbXSB9O1xufVxuXG5hbGxvd2VkVGFnc0Jhc2ljW1wiSU1HXCJdID0geyBhdHRyczogW1wiU1JDXCJdIH07XG5cbmFsbG93ZWRUYWdzRXh0ZW5kZWRbXCJBXCJdID0geyBhdHRyczogW1wiSFJFRlwiXSB9O1xuYWxsb3dlZFRhZ3NFeHRlbmRlZFtcIlRSXCJdID0geyBhdHRyczogW1wiUk9XU1BBTlwiXSB9O1xuYWxsb3dlZFRhZ3NFeHRlbmRlZFtcIlREXCJdID0geyBhdHRyczogW1wiQ09MU1BBTlwiLCBcIlJPV1NQQU5cIl0gfTtcbmFsbG93ZWRUYWdzRXh0ZW5kZWRbXCJUSFwiXSA9IHsgYXR0cnM6IFtcIkNPTFNQQU5cIiwgXCJST1dTUEFOXCJdIH07XG5hbGxvd2VkVGFnc0V4dGVuZGVkW1wiRk9OVFwiXSA9IHsgYXR0cnM6IFtcIkNPTE9SXCJdIH07XG5cbmNvbnN0IGFsbG93ZWRTdHlsaW5nID0ge1xuICAgIGNvbG9yOiB0cnVlLFxuICAgIFwiYmFja2dyb3VuZC1jb2xvclwiOiB0cnVlLFxuICAgIFwiZm9udC13ZWlnaHRcIjogdHJ1ZSxcbiAgICBcImZvbnQtc3R5bGVcIjogdHJ1ZSxcbiAgICBcInRleHQtZGVjb3JhdGlvbi1saW5lXCI6IHRydWUsXG59O1xuXG5sZXQgaXNOaWdodE1vZGUgPSBmdW5jdGlvbiAoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIGRvY3VtZW50LmJvZHkuY2xhc3NMaXN0LmNvbnRhaW5zKFwibmlnaHRNb2RlXCIpO1xufTtcblxubGV0IGZpbHRlckV4dGVybmFsU3BhbiA9IGZ1bmN0aW9uIChlbGVtOiBIVE1MRWxlbWVudCkge1xuICAgIC8vIGZpbHRlciBvdXQgYXR0cmlidXRlc1xuICAgIGZvciAoY29uc3QgYXR0ciBvZiBbLi4uZWxlbS5hdHRyaWJ1dGVzXSkge1xuICAgICAgICBjb25zdCBhdHRyTmFtZSA9IGF0dHIubmFtZS50b1VwcGVyQ2FzZSgpO1xuXG4gICAgICAgIGlmIChhdHRyTmFtZSAhPT0gXCJTVFlMRVwiKSB7XG4gICAgICAgICAgICBlbGVtLnJlbW92ZUF0dHJpYnV0ZU5vZGUoYXR0cik7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBmaWx0ZXIgc3R5bGluZ1xuICAgIGZvciAoY29uc3QgbmFtZSBvZiBbLi4uZWxlbS5zdHlsZV0pIHtcbiAgICAgICAgY29uc3QgdmFsdWUgPSBlbGVtLnN0eWxlLmdldFByb3BlcnR5VmFsdWUobmFtZSk7XG5cbiAgICAgICAgaWYgKFxuICAgICAgICAgICAgIWFsbG93ZWRTdHlsaW5nLmhhc093blByb3BlcnR5KG5hbWUpIHx8XG4gICAgICAgICAgICAvLyBnb29nbGUgZG9jcyBhZGRzIHRoaXMgdW5uZWNlc3NhcmlseVxuICAgICAgICAgICAgKG5hbWUgPT09IFwiYmFja2dyb3VuZC1jb2xvclwiICYmIHZhbHVlID09PSBcInRyYW5zcGFyZW50XCIpIHx8XG4gICAgICAgICAgICAvLyBpZ25vcmUgY29sb3VyZWQgdGV4dCBpbiBuaWdodCBtb2RlIGZvciBub3dcbiAgICAgICAgICAgIChpc05pZ2h0TW9kZSgpICYmIChuYW1lID09PSBcImJhY2tncm91bmQtY29sb3JcIiB8fCBuYW1lID09PSBcImNvbG9yXCIpKVxuICAgICAgICApIHtcbiAgICAgICAgICAgIGVsZW0uc3R5bGUucmVtb3ZlUHJvcGVydHkobmFtZSk7XG4gICAgICAgIH1cbiAgICB9XG59O1xuXG5hbGxvd2VkVGFnc0V4dGVuZGVkW1wiU1BBTlwiXSA9IGZpbHRlckV4dGVybmFsU3BhbjtcblxuLy8gYWRkIGJhc2ljIHRhZ3MgdG8gZXh0ZW5kZWRcbk9iamVjdC5hc3NpZ24oYWxsb3dlZFRhZ3NFeHRlbmRlZCwgYWxsb3dlZFRhZ3NCYXNpYyk7XG5cbmZ1bmN0aW9uIGlzSFRNTEVsZW1lbnQoZWxlbTogRWxlbWVudCk6IGVsZW0gaXMgSFRNTEVsZW1lbnQge1xuICAgIHJldHVybiBlbGVtIGluc3RhbmNlb2YgSFRNTEVsZW1lbnQ7XG59XG5cbi8vIGZpbHRlcmluZyBmcm9tIGFub3RoZXIgZmllbGRcbmxldCBmaWx0ZXJJbnRlcm5hbE5vZGUgPSBmdW5jdGlvbiAoZWxlbTogRWxlbWVudCkge1xuICAgIGlmIChpc0hUTUxFbGVtZW50KGVsZW0pKSB7XG4gICAgICAgIGVsZW0uc3R5bGUucmVtb3ZlUHJvcGVydHkoXCJiYWNrZ3JvdW5kLWNvbG9yXCIpO1xuICAgICAgICBlbGVtLnN0eWxlLnJlbW92ZVByb3BlcnR5KFwiZm9udC1zaXplXCIpO1xuICAgICAgICBlbGVtLnN0eWxlLnJlbW92ZVByb3BlcnR5KFwiZm9udC1mYW1pbHlcIik7XG4gICAgfVxuICAgIC8vIHJlY3Vyc2VcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IGVsZW0uY2hpbGRyZW4ubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgY29uc3QgY2hpbGQgPSBlbGVtLmNoaWxkcmVuW2ldO1xuICAgICAgICBmaWx0ZXJJbnRlcm5hbE5vZGUoY2hpbGQpO1xuICAgIH1cbn07XG5cbi8vIGZpbHRlcmluZyBmcm9tIGV4dGVybmFsIHNvdXJjZXNcbmxldCBmaWx0ZXJOb2RlID0gZnVuY3Rpb24gKG5vZGU6IE5vZGUsIGV4dGVuZGVkTW9kZTogYm9vbGVhbik6IHZvaWQge1xuICAgIGlmICghbm9kZUlzRWxlbWVudChub2RlKSkge1xuICAgICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gZGVzY2VuZCBmaXJzdCwgYW5kIHRha2UgYSBjb3B5IG9mIHRoZSBjaGlsZCBub2RlcyBhcyB0aGUgbG9vcCB3aWxsIHNraXBcbiAgICAvLyBlbGVtZW50cyBkdWUgdG8gbm9kZSBtb2RpZmljYXRpb25zIG90aGVyd2lzZVxuICAgIGZvciAoY29uc3QgY2hpbGQgb2YgWy4uLm5vZGUuY2hpbGRyZW5dKSB7XG4gICAgICAgIGZpbHRlck5vZGUoY2hpbGQsIGV4dGVuZGVkTW9kZSk7XG4gICAgfVxuXG4gICAgaWYgKG5vZGUudGFnTmFtZSA9PT0gXCJBTktJVE9QXCIpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IHRhZyA9IGV4dGVuZGVkTW9kZVxuICAgICAgICA/IGFsbG93ZWRUYWdzRXh0ZW5kZWRbbm9kZS50YWdOYW1lXVxuICAgICAgICA6IGFsbG93ZWRUYWdzQmFzaWNbbm9kZS50YWdOYW1lXTtcblxuICAgIGlmICghdGFnKSB7XG4gICAgICAgIGlmICghbm9kZS5pbm5lckhUTUwgfHwgbm9kZS50YWdOYW1lID09PSBcIlRJVExFXCIpIHtcbiAgICAgICAgICAgIG5vZGUucGFyZW50Tm9kZS5yZW1vdmVDaGlsZChub2RlKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIG5vZGUub3V0ZXJIVE1MID0gbm9kZS5pbm5lckhUTUw7XG4gICAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgICBpZiAodHlwZW9mIHRhZyA9PT0gXCJmdW5jdGlvblwiKSB7XG4gICAgICAgICAgICAvLyBmaWx0ZXJpbmcgZnVuY3Rpb24gcHJvdmlkZWRcbiAgICAgICAgICAgIHRhZyhub2RlKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIC8vIGFsbG93ZWQsIGZpbHRlciBvdXQgYXR0cmlidXRlc1xuICAgICAgICAgICAgZm9yIChjb25zdCBhdHRyIG9mIFsuLi5ub2RlLmF0dHJpYnV0ZXNdKSB7XG4gICAgICAgICAgICAgICAgY29uc3QgYXR0ck5hbWUgPSBhdHRyLm5hbWUudG9VcHBlckNhc2UoKTtcbiAgICAgICAgICAgICAgICBpZiAodGFnLmF0dHJzLmluZGV4T2YoYXR0ck5hbWUpID09PSAtMSkge1xuICAgICAgICAgICAgICAgICAgICBub2RlLnJlbW92ZUF0dHJpYnV0ZU5vZGUoYXR0cik7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxufTtcbiJdfQ==