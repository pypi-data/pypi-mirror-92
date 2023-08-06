define([
    'nbextensions/visualpython/src/common/StringBuilder'
    , './api.js'
    , './constData.js'
    , './createBlockBtn.js'
    , './api_list.js'
    , 'nbextensions/visualpython/src/common/constant'
], function ( sb, api, constData, createBlockBtn, api_list, vpConst ) {

    const { RenderHTMLDomColor } = api;
    const {  BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION

            , VP_CLASS_PREFIX
            , VP_CLASS_APIBLOCK_MAIN    
            , VP_CLASS_APIBLOCK_BOARD
        
            , STR_CLICK } = constData;  

    const { api_listInit 
        , libraryLoadCallback
        , toggleApiListSubGroupShow
        , makeOptionPageNaviInfo
        , loadLibraries
        , getNavigationInfo } = api_list;
        
    const CreateBlockBtn = createBlockBtn;

    var CreateApiBtn = function(blockContainerThis, funcID, name, grpName) { 
        this.blockContainerThis = blockContainerThis;
        this.type = constData.BLOCK_CODELINE_TYPE.API;

        this.funcID = funcID;
        this.name = name;
        this.grpName = grpName;

        this.createBlockBtnDom = null;
        this.render();
        this.bindApiClickEvent();
    }

    /**
     * CreateBlockBtn 에서 상속
     */
    CreateApiBtn.prototype = Object.create(CreateBlockBtn.prototype);

    CreateApiBtn.prototype.getName = function() { return this.name; }
    CreateApiBtn.prototype.getGrpName = function() { return this.grpName; }

    CreateApiBtn.prototype.setName = function(name) { this.name = name; }
    CreateApiBtn.prototype.setGrpName = function(grpName) { this.grpName = grpName; }

    CreateApiBtn.prototype.render = function() {
        var sbCreateBlockBtn = new sb.StringBuilder();
        // sbCreateBlockBtn.appendFormatLine("<div class='{0}'>",'vp-apiblock-tab-navigation-node-block-body-btn');
        sbCreateBlockBtn.appendFormatLine("<div class='{0}'>", 'vp-apiblock-tab-navigation-node-block-body-btn api');
        sbCreateBlockBtn.appendFormatLine("<span class='{0}' title='{1}'>",'vp-block-name', this.getName());
        sbCreateBlockBtn.appendFormatLine("{0}", this.getName());
        sbCreateBlockBtn.appendLine("</span>");
        sbCreateBlockBtn.appendLine("</div>");

        var createBlockContainer = null;

        /** API - define */
        createBlockContainer = $(`.vp-apiblock-left-tab-` + this.getGrpName());
  
        var createBlockBtnDom = $(sbCreateBlockBtn.toString());
        this.setBlockMainDom(createBlockBtnDom);
        // createBlockBtnDom = RenderHTMLDomColor(this, createBlockBtnDom);

        createBlockContainer.append(createBlockBtnDom);

        this.createBlockBtnDom = createBlockBtnDom;
    }

    CreateBlockBtn.prototype.bindApiClickEvent = function() {
        var blockContainerThis = this.blockContainerThis;
        var funcID = this.funcID;
        $(this.createBlockBtnDom).on(STR_CLICK, function(event) {
            event.stopPropagation();
            var naviInfo = getNavigationInfo(funcID);

            /** board에 선택한 API List 블럭 생성 */
            blockContainerThis.createAPIListBlock(funcID, naviInfo);
        });
    }

    return CreateApiBtn;
});