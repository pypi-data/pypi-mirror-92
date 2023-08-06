define([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/common/metaDataHandler'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , './shadowBlock.js'
    , './api.js'
    , './api_list.js'
    , './constData.js'
    , './block.js'
], function ( vpCommon, vpFuncJS, md, vpConst, sb,
              shadowBlock, api, api_list, constData, block ) {

    const { RemoveSomeBlockAndGetBlockList
        
            , IsCodeBlockType
            , IsCanHaveIndentBlock     
            , RenderHTMLDomColor
    
            , GenerateClassInParamList
            , GenerateDefInParamList
            , GenerateReturnOutParamList
            , GenerateIfConditionList
            , GenerateExceptConditionList
            , GenerateForParam
            , GenerateLambdaParamList

            , GenerateWhileConditionList

            , ShowImportListAtBlock
            , ShowCodeBlockCode  } = api;

    const {  BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , FOCUSED_PAGE_TYPE
            , DEF_BLOCK_ARG6_TYPE
            
            , STR_CHANGE_KEYUP_PASTE
            , STR_COLON_SELECTED 

            , VP_CLASS_PREFIX 

            , VP_CLASS_BLOCK_NUM_INFO
            , VP_CLASS_BLOCK_CONTAINER

            , VP_CLASS_BLOCK_HEADER_PARAM
            , VP_CLASS_APIBLOCK_MAIN
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_BOARD_CONTAINER
            , VP_CLASS_APIBLOCK_BUTTONS
            , VP_CLASS_APIBLOCK_OPTION_TAB
            , VP_CLASS_APIBLOCK_CODELINE_ELLIPSIS
            , VP_CLASS_APIBLOCK_INPUT_PARAM
            , VP_CLASS_APIBLOCK_MENU_BTN
            , VP_CLASS_APIBLOCK_OPTION_TAB_SELECTOR
            , VP_CLASS_BLOCK_SUB_BTN_CONTAINER
            , VP_CLASS_SELECTED_SHADOWBLOCK 
            , VP_CLASS_BLOCK_BOTTOM_HOLDER
            , VP_CLASS_STYLE_DISPLAY_NONE
            , VP_CLASS_APIBLOCK_NODEBLOCK
            , VP_CLASS_APIBLOCK_BLOCK_HEADER

            , VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF

            , VP_ID_PREFIX
            , VP_ID_WRAPPER

            , NUM_INDENT_DEPTH_PX
            , NUM_MAX_ITERATION
            , NUM_DEFAULT_POS_Y
            , NUM_DEFAULT_POS_X
            , NUM_MAX_BLOCK_NUMBER
            , NUM_NODE_OR_TEXT_BLOCK_MARGIN_TOP_PX
            , NUM_BLOCK_MAX_WIDTH
            , NUM_TEXT_BLOCK_WIDTH
            , NUM_OPTION_PAGE_WIDTH
            , NUM_BUTTONS_PAGE_WIDTH
            , NUM_API_BOARD_CENTER_PAGE_WIDTH
            , NUM_API_BOARD_CENTER_PAGE_MIN_WIDTH
            
            , VP_BLOCK
            , VP_CLASS_BLOCK_CODETYPE_NAME
        
            , NUM_SHADOWBLOCK_OPACITY
        
            , STR_100PERCENT
            , STR_POSITION
            , STR_RELATIVE

            , STR_EMPTY
            , STR_TOP
            , STR_LEFT
            , STR_DIV
            , STR_ONE_SPACE
            , STR_DOT
            , STR_SCROLLHEIGHT
            , STR_DATA_NUM_ID
            , STR_PX
            , STR_BORDER
            , STR_HEIGHT
            , STR_SPAN
            , STR_WIDTH
            , STR_MARGIN_LEFT
            , STR_MAX_WIDTH
            , STR_MIN_WIDTH
            , STR_KEYWORD_NEW_LINE
            , STR_ONE_INDENT
            , STR_CLICK
            , STR_COLOR
            , STR_BOX_SHADOW
            , STR_BACKGROUND_COLOR 
            , STR_DATA_DEPTH_ID 
            , STR_TRANSPARENT
            
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_CODE
            , STR_PROPERTY
            , STR_OPACITY
            , STR_MSG_AUTO_GENERATED_BY_VISUALPYTHON
  
            , STR_DISPLAY
            , STR_BLOCK
            , STR_RIGHT
            , STR_NONE 
            , STR_FLEX 

            , STATE_className
            , STATE_classInParamList
            , STATE_defInParamList
            , STATE_returnOutParamList

            , STATE_elifCodeLine
            , STATE_exceptCodeLine

            , STATE_breakCodeLine
            , STATE_continueCodeLine
            , STATE_passCodeLine
            , STATE_codeLine
            , STATE_propertyCodeLine
   

            , STATE_isIfElse
            , STATE_isForElse
            , STATE_isFinally

            , STATE_defName
            , STATE_state

            , COLOR_CLASS_DEF
            , COLOR_CONTROL
            , COLOR_CODE
            , COLOR_FOCUSED_PAGE
            , COLOR_WHITE
            , API_BLOCK_PROCESS_DEVELOPMENT
        
            , ERROR_AB0002_INFINITE_LOOP } = constData;
 
    const { Block } = block;
    const ShadowBlock = shadowBlock; 

    const { api_listInit
            , setClosureBlock
            , loadOption_block
            , loadOption_textBlock
            , optionPageLoadCallback_block
            , makeUpGreenRoomHTML  } = api_list;

    var BlockContainer = function() {
        this.importPackageThis = null;

        this.blockList = [];
        this.nodeBlockList = [];
        this.textBlockList = [];
        this.prevBlockList = [];
        this.loadedVariableList = [];

        this.isBlockDoubleClicked = false; //

        // API Block 햄버거 메뉴바를 open하면 true, close하면 false
        this.isMenubarOpen = false; 

        /**  API Block 햄버거 메뉴에서 depth를 보여줄지 말지 결정 가능 
         *  true면 보여주고 false면 안 보여줌
         */
        this.isShowDepth = true;  

        /** API List를 보여줄지 말지 결정 
         *  true면 보여주고 false면 안 보여줌
         */
        this.isAPIListPageOpen = true; 

        /** option popup을 resize하면 true
         * resize가 끝나면 false
         * 
         * option popup이 끝난 상태(isOptionPageResize = false) 이어야
         * visual python 전체 resize 기능 가능
         */
        this.isOptionPageResize = false; 

        this.classNum = 1;
        this.defNum = 1;
        this.nodeBlockNumber = 0;

        /** 현재 작업하고 있는 API Block 영역의 데이터를 저장 
         * 영역은 총 4가지 FOCUSED_PAGE_TYPE
        */
        this.focusedPageType = null;

        /** option popup의 width값 지정 
         * 이후 resize를 통해 늘어나거나 줄어들 수 있음 
        */
        this.optionPageWidth = NUM_OPTION_PAGE_WIDTH;

        /** block의 width 값. 기본은 300. 
         * 이후 resize를 통해 늘어나거나 줄어들 수 있음 */
        this.blockMaxWidth = NUM_BLOCK_MAX_WIDTH;

        this.scrollHeight = 0;
        // this.isStopMoveScrollHeight = false;

        /** 현재 작업 중이거나, 클릭한 블럭을 selectedBlock에 저장함 
         *  현재 작업 중이거나, 클릭한 블럭이 무엇인지 알기 위해서 필요
         */
        this.selectedBlock = null;

        this.blockContainerDom = null;

        /** generateCode를 실행하면 이 데이터로 실행 */
        this.code = STR_EMPTY;

        this.mdHandler = null;  

        this.domPool = new Map();
    }

    BlockContainer.prototype.setMetahandler = function(funcID) {
        this.mdHandler = new md.MdHandler(funcID); 
    }

    BlockContainer.prototype.setImportPackageThis = function(importPackageThis) {
        this.importPackageThis = importPackageThis;
    }

    BlockContainer.prototype.getImportPackageThis = function() {
        return this.importPackageThis;
    }

    BlockContainer.prototype.setIsBlockDoubleClicked = function(isBlockDoubleClicked) {
        this.isBlockDoubleClicked = isBlockDoubleClicked;
    }

    BlockContainer.prototype.getIsBlockDoubleClicked = function() {
        return this.isBlockDoubleClicked;
    }

    BlockContainer.prototype.setIsMenubarOpen = function(isMenubarOpen) {
        this.isMenubarOpen = isMenubarOpen;
    }
    BlockContainer.prototype.getIsMenubarOpen = function() {
        return this.isMenubarOpen;
    }

    BlockContainer.prototype.setIsShowDepth = function(isShowDepth) {
        this.isShowDepth = isShowDepth;
    }
    BlockContainer.prototype.getIsShowDepth = function() {
        return this.isShowDepth;
    }


    BlockContainer.prototype.setIsAPIListPageOpen = function(isAPIListPageOpen) {
        this.isAPIListPageOpen = isAPIListPageOpen;
    }
    BlockContainer.prototype.getIsAPIListPageOpen = function() {
        return this.isAPIListPageOpen;
    }
    
    BlockContainer.prototype.setIsOptionPageResize = function(isOptionPageResize) {
        this.isOptionPageResize = isOptionPageResize;
    }
    BlockContainer.prototype.getIsOptionPageResize = function() {
        return this.isOptionPageResize;
    }

    BlockContainer.prototype.setOptionPageWidth = function(optionPageWidth) {
        this.optionPageWidth = optionPageWidth;
    }
    BlockContainer.prototype.getOptionPageWidth = function() {
        return this.optionPageWidth;
    }

    BlockContainer.prototype.setBlockMaxWidth = function(blockMaxWidth) {
        this.blockMaxWidth = blockMaxWidth;
    }
    BlockContainer.prototype.getBlockMaxWidth = function() {
        return this.blockMaxWidth;
    }

    /** Block 생성
     * @param {string} blockType 생성할 블럭의 타입 ex) class, def, if ...
     * 
     * @option
     * @param {Object} blockData vpnote을 open할 때 vpnote에 담긴 데이터를 기반으로 블럭을 생성
     */
    BlockContainer.prototype.createBlock = function(blockType, blockData = null) {
        var thisBlock =  new Block(this, blockType, blockData);
        return thisBlock;
    }

    /** Logic에서 Block을 드래그해서 생성 할 때 */
    BlockContainer.prototype.createBlock_first = function(thisBlock) {
        var blockType = thisBlock.getBlockType();
        if (blockType == BLOCK_CODELINE_TYPE.CLASS) {
            var defBlock = this.createBlock(BLOCK_CODELINE_TYPE.DEF);
            defBlock.setState({
                defName: '__init__'
            });
            var newData = {
                arg3: 'self'
                , arg4: STR_EMPTY
                , arg5: STR_EMPTY
                , arg6: DEF_BLOCK_ARG6_TYPE.NONE
            }
            var inParamList = thisBlock.getState(STATE_defInParamList);
            defBlock.setState({
                [STATE_defInParamList]: [ ...inParamList, newData ]
            });
            defBlock.init();
            var defBlockMainDom = defBlock.getBlockMainDom();
            RenderHTMLDomColor(defBlock, defBlockMainDom);

            var holderBlock = this.createBlock(BLOCK_CODELINE_TYPE.HOLDER );

            thisBlock.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
            thisBlock.appendBlock(defBlock, BLOCK_DIRECTION.INDENT);

            $(holderBlock.getBlockMainDom()).addClass(VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF);
            $(holderBlock.getBlockMainDom()).css(STR_BACKGROUND_COLOR, COLOR_CLASS_DEF);

        /** def block일 경우 */
        } else if ( blockType == BLOCK_CODELINE_TYPE.DEF) {
            
            var returnBlock = this.createBlock( BLOCK_CODELINE_TYPE.RETURN );
            var holderBlock = this.createBlock( BLOCK_CODELINE_TYPE.HOLDER );
            
            thisBlock.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
            thisBlock.appendBlock(returnBlock, BLOCK_DIRECTION.INDENT);

            $(holderBlock.getBlockMainDom()).addClass(VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF);
            $(holderBlock.getBlockMainDom()).css(STR_BACKGROUND_COLOR, COLOR_CLASS_DEF);

        /** if, for, while, try block일 경우 */
        } else if ( blockType == BLOCK_CODELINE_TYPE.IF 
                    || blockType == BLOCK_CODELINE_TYPE.FOR 
                    || blockType == BLOCK_CODELINE_TYPE.WHILE 
                    || blockType == BLOCK_CODELINE_TYPE.TRY 
                    || blockType == BLOCK_CODELINE_TYPE.ELSE 
                    || blockType == BLOCK_CODELINE_TYPE.ELIF 
                    || blockType == BLOCK_CODELINE_TYPE.FOR_ELSE 
                    || blockType == BLOCK_CODELINE_TYPE.EXCEPT 
                    || blockType == BLOCK_CODELINE_TYPE.FINALLY ) {

            var passBlock = this.createBlock( BLOCK_CODELINE_TYPE.PASS);
            var holderBlock = this.createBlock( BLOCK_CODELINE_TYPE.HOLDER );
            
            thisBlock.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
            thisBlock.appendBlock(passBlock, BLOCK_DIRECTION.INDENT);
        } 
    }

    /** block을 blockList에 add */
    BlockContainer.prototype.addBlock = function(block) {
        this.blockList = [...this.blockList, block];
    }

    /** blockList를 가져옴*/
    BlockContainer.prototype.getBlockList = function() {
        return this.blockList;
    }
    /** blockList를 파라미터로 받은 blockList로 덮어 씌움*/
    BlockContainer.prototype.setBlockList = function(blockList) {
        this.blockList = blockList;
    }

    BlockContainer.prototype.getNodeBlockList = function() {
        return this.nodeBlockList;
    }

    BlockContainer.prototype.getNodeBlockList_asc = function() {
        var rootBlock = this.getRootBlock();
        var blockChildList = rootBlock.getThisToLastBlockList();
        var nodeBlockList = [];
        blockChildList.forEach((block, index) => {
            if (block.getBlockType() == BLOCK_CODELINE_TYPE.NODE) {
                nodeBlockList.push(block);
            } 
        });
        return nodeBlockList;
    }

    BlockContainer.prototype.getNodeBlockAndTextBlockList_asc = function() {
        var rootBlock = this.getRootBlock();
        var blockChildList = rootBlock.getThisToLastBlockList();
        var nodeBlockList = [];
        blockChildList.forEach((block, index) => {
            if (block.getBlockType() == BLOCK_CODELINE_TYPE.NODE
                || block.getBlockType() == BLOCK_CODELINE_TYPE.TEXT) {
                nodeBlockList.push(block);
            } 
        });
        return nodeBlockList;
    }

    BlockContainer.prototype.setNodeBlockList = function(nodeBlockList) {
        this.nodeBlockList = nodeBlockList;
    }

    /** block을 blockList에 add */
    BlockContainer.prototype.addNodeBlock = function(block) {
        this.addNodeBlockNumber();
        this.nodeBlockList = [...this.nodeBlockList, block];
    }

    BlockContainer.prototype.getTextBlockList = function() {
        return this.textBlockList;
    }
    BlockContainer.prototype.setTextBlockList = function(textBlockList) {
        this.textBlockList = textBlockList;
    }

    /** block을 blockList에 add */
    BlockContainer.prototype.addTextBlock = function(block) {
        this.textBlockList = [...this.textBlockList, block];
    }
    
    /** prevBlockList를 가져옴*/
    BlockContainer.prototype.getPrevBlockList = function() {
        return this.prevBlockList;
    }
    /** prevBlockList를 파라미터로 받은 prevBlockList로 덮어 씌움*/
    BlockContainer.prototype.setPrevBlockList = function(prevBlockList) {
        this.prevBlockList = prevBlockList;
    }

    /** root block을 get */
    BlockContainer.prototype.getRootBlock = function() {
        var blockList = this.getBlockList();

        var rootBlock = null;
        blockList.some(block => {
            if (block.getDirection() == BLOCK_DIRECTION.ROOT) {
                rootBlock = block;
                return true;
            }
        });
        return rootBlock;
    }

    BlockContainer.prototype.setClassNum = function(classNum) {
        this.classNum = classNum;
    }
    BlockContainer.prototype.addClassNum = function() {
        this.classNum += 1;
    }
    BlockContainer.prototype.getClassNum = function() {
        return this.classNum;
    }

    BlockContainer.prototype.setDefNum = function(defNum) {
        this.defNum = defNum;
    }
    BlockContainer.prototype.addDefNum = function() {
        this.defNum += 1;
    }
    BlockContainer.prototype.getDefNum = function() {
        return this.defNum;
    }


    BlockContainer.prototype.setNodeBlockNumber = function(nodeBlockNumber) {
        this.nodeBlockNumber = nodeBlockNumber;
    }
    BlockContainer.prototype.addNodeBlockNumber = function() {
        this.nodeBlockNumber += 1;
    }
    BlockContainer.prototype.getNodeBlockNumber = function() {
        return this.nodeBlockNumber;
    }

    BlockContainer.prototype.getMaxWidth = function() {
        var maxWidth = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD_CONTAINER)).width();
        return maxWidth;
    }

    BlockContainer.prototype.getMaxHeight = function() {
        var maxHeight = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD_CONTAINER)).height();
        return maxHeight;
    }

    BlockContainer.prototype.getScrollHeight = function() {
        return this.scrollHeight;
    }
    BlockContainer.prototype.setScrollHeight = function(scrollHeight) {
        this.scrollHeight = scrollHeight;
    }

    // BlockContainer.prototype.getIsStopMoveScrollHeight = function() {
    //     return this.isStopMoveScrollHeight;
    // }
    // BlockContainer.prototype.setIsStopMoveScrollHeight = function(isStopMoveScrollHeight) {
    //     this.isStopMoveScrollHeight = isStopMoveScrollHeight;
    // }

    BlockContainer.prototype.setBlockContainerDom = function(blockContainerDom) {
        this.blockContainerDom = blockContainerDom;
    }
    BlockContainer.prototype.getBlockContainerDom = function() {
        return this.blockContainerDom;
    }

    BlockContainer.prototype.setSelectBlock = function(selectedBlock) {
        this.selectedBlock = selectedBlock;
    }
    BlockContainer.prototype.getSelectBlock = function() {
        return this.selectedBlock;
    }

    BlockContainer.prototype.getAPIBlockCode = function() {
        return this.code;
    }
    BlockContainer.prototype.setAPIBlockCode = function(code) {
        this.code = code;
    }
    
    BlockContainer.prototype.setFocusedPageType = function(focusedPageType) {
        this.focusedPageType = focusedPageType;
    }
    BlockContainer.prototype.getFocusedPageType = function() {
        return this.focusedPageType;
    }

    /**
     * API Block은 크게 4가지 영역으로 나뉨
     * 1. Logic
     * 2. Board 
     * 3.     - Board 위에 node 블럭 생성 input 칸
     * 4. Option popup
     * 
     * 각 영역에서 작업을 할 때, 
     * 내부적으로 focus해서 어느 영역에서 작업하는지 알고 있기 위해 FocusedPageType 지정
     * 예전에는 초록색 border로 영역을 지정했으니 현재는 삭제하여 보여지지는 않음
     * @param {ENUM} focusedPageType 
     */
    BlockContainer.prototype.setFocusedPageTypeAndRender = function(focusedPageType) {
        this.setFocusedPageType(focusedPageType);
    }

    /** 블럭 데이터 복사 */
    BlockContainer.prototype.setCtrlSaveData = function() {
        var selectedBlock = this.getSelectBlock();
        var lastBlock = selectedBlock.getLastBlock_from_nodeBlockArea();
        var childBlockList = selectedBlock.getBlockList_nodeBlockArea();
        
        var blockList_cloned = this.copyBlockList(childBlockList);
        var lastCopyBlocklist_cloned = blockList_cloned[0];

        this.lastBlock = lastBlock;
        this.lastCopyBlocklist_cloned = lastCopyBlocklist_cloned;
    }

    /** 복사한 블럭 데이터 가져옴 */
    BlockContainer.prototype.getCtrlSaveData = function() {
        return {
            lastBlock: this.lastBlock
            , lastCopyBlocklist_cloned: this.lastCopyBlocklist_cloned
        }
    }

    /** blockList에서 특정 block을 삭제
     * @param {string} blockUUID
     */
    BlockContainer.prototype.deleteBlock = function(blockUUID) {
        /** blockList를 돌며 삭제하고자 하는 block을 찾아 제거
         */
        var blockList = this.getBlockList();
        blockList.some((block, index) => {
            if (block.getUUID() == blockUUID) {
                delectedIndex = index;
                blockList.splice(index, 1);
                return true;
            } else {
                return false;
            }
        });
    }

    /** Blocklist의 block들 전부삭제 */
    BlockContainer.prototype.deleteAllBlock = function() {
        var blockList = this.getBlockList();
        blockList.forEach(block => {
            block.reConnectPrevBlock();
            block.deleteBlockDomAndData();
        });
        this.setBlockList([]);
        this.setPrevBlockList([]);
    }

    /** nodeBlockList에서 특정 block을 삭제
     * @param {string} blockUUID
     */
    BlockContainer.prototype.deleteNodeBlock = function(blockUUID) {
        var nodeBlockList = this.getNodeBlockList();
        nodeBlockList.some((block, index) => {
            if (block.getUUID() == blockUUID) {
                nodeBlockList.splice(index, 1);
                return true;
            } else {
                return false;
            }
        });
    }

    BlockContainer.prototype.makeAPIBlockMetadata = function() {
        var rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return [];
        }

        var childBlockList = rootBlock.getThisToLastBlockList();
        var apiBlockJsonDataList = this.blockToJson(childBlockList);
        return apiBlockJsonDataList;
    }

    /** Block을 json 데이터로 변환 */
    BlockContainer.prototype.blockToJson = function(blockList) {
        var apiBlockJsonDataList = [];
        blockList.forEach( (block, index) => {
            if (block.getBlockType() == BLOCK_CODELINE_TYPE.API) {
                block.setMetadata();
            }
            // console.log('block',block);
            // console.log('block.state',block.state);

            /** 자식 블럭 리스트 중에 uuid만 뽑아서 리턴 */
            var nextBlockUUIDList = block.getChildBlockList().map(nextBlock => {
                return nextBlock.getUUID();
            });
            apiBlockJsonDataList[index] = {
                UUID: block.getUUID()
                , nextBlockUUIDList
                , blockType: block.getBlockType()
                , blockName: block.getBlockName()
                , blockOptionState: block.state
                , blockDepth: block.getDepth()
                , blockDirection: block.getDirection()
            }
        });
        return apiBlockJsonDataList;
    }

    /** json을 Block 데이터로 변환 */
    BlockContainer.prototype.jsonToBlock = function(apiBlockJsonDataList) {
        var createdBlockList = [];
        var createdBlock = null;
        apiBlockJsonDataList.forEach( (blockData, index) => {
            const { UUID, nextBlockUUIDList
                     , blockType, blockName, blockOptionState, blockDepth, blockDirection } = blockData;

            createdBlock = this.createBlock(blockType, blockData);
            createdBlock.setUUID(UUID);
            createdBlock.setDepth(blockDepth);
            createdBlock.setDirection(blockDirection);
            createdBlock.setBlockName(blockName);
            createdBlock.state = blockOptionState;
            createdBlock.setNextBlockUUIDList(nextBlockUUIDList);
            
            createdBlockList.push(createdBlock);
        });

        var nextBlockUUIDList = [];
        createdBlockList.forEach((createdBlock,index) => {
            nextBlockUUIDList = createdBlock.getNextBlockUUIDList();
            nextBlockUUIDList.forEach(uuid => {
                createdBlockList.forEach(nextCreatedBlock => {
                    if (uuid == nextCreatedBlock.getUUID()) {
                        nextCreatedBlock.setPrevBlock(createdBlock);
                        createdBlock.addChildBlockList(nextCreatedBlock);
                    }           
                });
            });
        });
        return createdBlockList;
    }

    BlockContainer.prototype.copyBlockList = function(copyedBlockList) {
        var apiBlockJsonDataList = this.blockToJson(copyedBlockList);

        var uuid_hable = [];
        apiBlockJsonDataList.forEach((blockData,index) => {
            const { UUID } = blockData;
            uuid_hable[UUID] = {
                oldUUID: UUID
                , newUUID: vpCommon.getUUID()
            }
        });

        apiBlockJsonDataList.forEach((blockData,index) => {
            var newNextBlockUUIDList = [];
            blockData.nextBlockUUIDList.forEach(uuid => {
                if (uuid_hable[uuid] != undefined) {
                    newNextBlockUUIDList.push(uuid_hable[uuid].newUUID);
                }
            });

            blockData.nextBlockUUIDList = newNextBlockUUIDList;
            blockData.UUID = uuid_hable[blockData.UUID].newUUID;
        });
        uuid_hable = [];
        

        var createdBlockList = this.jsonToBlock(apiBlockJsonDataList);
        return createdBlockList;
    }

    /** 
     * @async
     * Block editor에 존재하는 블럭들을 
     * (이전) prevBlockList 데이터와
     * (현재) blockList 데이터를 기반으로
     * 전부 다시 렌더링한다 
     */
    BlockContainer.prototype.reRenderBlockList = async function(isMetaData) {
        // console.log('reRenderBlockList');
        var blockContainerThis = this;
        var prevBlockList = this.getPrevBlockList();

        var rootBlock = this.getRootBlock();
        if (rootBlock == null) {
            return;
        }

        //** root Block의 자식 Block depth 계산하고 표시 */
        var blockList = rootBlock.getThisToLastBlockList();
        blockList.forEach(async (block, index) => {
            var depth = block.calculateDepthAndGet();
            block.setDepth(depth);
  
            var indentPxNum = block.getIndentNumber();
            var numWidth = 0;
            /** TEXT 블럭과 그 외 일반 블럭의 WIDTH값을 다르게 함 */
            if (block.getBlockType() == BLOCK_CODELINE_TYPE.TEXT) {
                numWidth = NUM_TEXT_BLOCK_WIDTH;
            } else {
                numWidth = this.getBlockMaxWidth() - indentPxNum;
            }

            var blockMainDom = block.getBlockMainDom();
            $(blockMainDom).css(STR_MARGIN_LEFT, indentPxNum);
            $(blockMainDom).css(STR_WIDTH, numWidth);
        });

        // console.log('prevBlockList',prevBlockList);
        // console.log('blockList',blockList);

        /** metadata를 받아서 reRender */
        if (isMetaData == true) {
            // console.log('isMetaData == true');
            var containerDom = blockContainerThis.reNewContainerDom();
            for await (var block of blockList) {
                new Promise( (resolve) => resolve( $(containerDom).append(block.getBlockMainDom())));
                block.bindEventAll();
            }
        /** blockList 길이 < prevBlockList 길이 */
        } else if ( blockList < prevBlockList ) {
            // console.log('blockList < prevBlockList');
            var deletedBlockList = RemoveSomeBlockAndGetBlockList(prevBlockList, blockList);
            deletedBlockList.forEach(block => {
               var blockMainDom = block.getBlockMainDom();
               $(blockMainDom).remove();
            });
        /** blockList 길이 > prevBlockList 길이 */
        } else if (blockList > prevBlockList) {
            // console.log('blockList > prevBlockList');
            var containerDom = this.getBlockContainerDom();
            var addedBlockList = RemoveSomeBlockAndGetBlockList(blockList, prevBlockList);
            var prevBlock = addedBlockList[0].getPrevBlock();
            if (prevBlock === null) {
               addedBlockList.forEach((addedBlock,index) => {
                   $(containerDom).append(addedBlock.getBlockMainDom() );
                   addedBlock.bindEventAll();
               });
           } else {
               addedBlockList.forEach(addedBlock => {
                   $( addedBlock.getBlockMainDom() ).insertAfter(prevBlock.getBlockMainDom());
                   addedBlock.bindEventAll();
                   prevBlock = addedBlock;
               });
           }
        } else {
            // console.log('');
            var containerDom = blockContainerThis.reNewContainerDom();
            for await (var block of blockList) {
                new Promise( (resolve) => resolve( $(containerDom).append(block.getBlockMainDom())));
                block.bindEventAll();
            }
        }

        this.setPrevBlockList(blockList);
    }

    BlockContainer.prototype.reRenderBlockList_fromMetadata = function(apiBlockJsonDataList) {
    
        this.reNewContainerDom();
        /** metadata json을 기반으로 블럭 렌더링 */
        var createdBlockList = this.jsonToBlock(apiBlockJsonDataList);
        
        this.deleteAllOptionDom();
        this.setBlockList(createdBlockList);
        this.reRenderAllBlock_metadata();

        /** text 블럭일 경우 
         *  Markdown pakage를 생성해서 text 블럭에 넣어주고,
         *  text 블럭 preview에 Markdown 형식의 preview Render를 한다.
         */
        createdBlockList.forEach(block => {
            var blockType = block.getBlockType();
            if (blockType == BLOCK_CODELINE_TYPE.TEXT) {
                const textBlockFuncID = 'com_markdown';
                loadOption_textBlock(textBlockFuncID, (markdownPakage) => {
                    block.setImportPakage(markdownPakage);
                    markdownPakage.setBlock(block);
                
                    /** option popup 생성 */
                    var blockOptionPageDom = makeUpGreenRoomHTML();
                    /** text 블럭 데이터 */
                    var text = block.getState(STATE_codeLine);
        
                    block.setBlockOptionPageDom(blockOptionPageDom);

                    /** text 블럭 preview에 Markdown 형식의 preview Render */
                    markdownPakage.bindOptionEvent();
                    markdownPakage.previewRender(block.getImportPakage().uuid, text);
        
                    /** option popup에 있는 textarea에 text 블럭 데이터 넣기 */
                    const textarea = block.getBlockOptionPageDom().find(`#vp_markdownEditor`).get(0);
                    $(textarea).val(text);

                    this.resetOptionPage();
                });
            } 
        });

        this.resetOptionPage();
    }

     /** Block 앞에 line number를 정렬
      * isAsc true면 오름차순 정렬
     */
     BlockContainer.prototype.renderBlockLineNumberInfoDom = async function(isAsc) {
        var rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return;
        }

        /** 0 depth는 opacity 0으로 처리
         *  1 이상의 depth는 opacity 1로 처리
         */
        var blockChildList = rootBlock.getThisToLastBlockList();
        blockChildList.forEach(block => {
            var blockDepthInfoDom = block.getBlockDepthInfoDom();
            if (block.getDepth() == 0) {
                var blockDepthInfoDom = block.getBlockDepthInfoDom();
                $(blockDepthInfoDom).css(STR_OPACITY,0);
            } else {
                $(blockDepthInfoDom).css(STR_OPACITY,1);
            }
        });

        var nodeBlockOrTextBlockList = this.getNodeBlockAndTextBlockList_asc();
        nodeBlockOrTextBlockList.forEach(block => {
            var $blockLineNumberInfoDom = $(block.getBlockLineNumberInfoDom());
            $blockLineNumberInfoDom.css( STR_LEFT, -NUM_DEFAULT_POS_X );
            $blockLineNumberInfoDom.css(STR_OPACITY, 1);
        });

        var nodeBlockList = this.getNodeBlockList_asc();
        nodeBlockList.forEach(async (block, index) => {
            if (block.getIsNodeBlockToggled() == true){
                $(block.getBlockMainDom()).css(STR_BOX_SHADOW,'0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)');
            } else {
                $(block.getBlockMainDom()).css(STR_BOX_SHADOW, STR_NONE);
            }
         
            var $blockLineNumberInfoDom = $(block.getBlockLineNumberInfoDom());
            var blockLineNumber = 0;

            /** Line number 오름차순 정렬의 경우 */
            if (isAsc == true) {
                $blockLineNumberInfoDom.css(STR_COLOR, '#828282');
                blockLineNumber = index + 1;
            /** 처음 생성한 Line number를 그대로 보여줄 경우 */
            } else {
                blockLineNumber = block.getBlockNumber();
            }

            block.setBlockNumber(blockLineNumber);

            if (blockLineNumber >= NUM_MAX_BLOCK_NUMBER) {
                blockLineNumber = NUM_MAX_BLOCK_NUMBER;
            }

            $blockLineNumberInfoDom.text(block.getBlockNumber());
        });
    }
    
    BlockContainer.prototype.reRenderAllBlock = function() {
        this.calculateDepthAndSetDepth();
        this.reRenderBlockList();
        this.renderBlockLineNumberInfoDom();
    }
    
    BlockContainer.prototype.reRenderAllBlock_asc = function() {
        this.calculateDepthAndSetDepth();
        this.reRenderBlockList();
        this.renderBlockLineNumberInfoDom(true);
    }

    BlockContainer.prototype.reRenderAllBlock_metadata = function() {
        this.calculateDepthAndSetDepth();
        this.reRenderBlockList(true);
        this.renderBlockLineNumberInfoDom(true);
    }

    /**
     */
    BlockContainer.prototype.getRootToLastBottomBlock = function() {
        var rootBlock = this.getRootBlock();
        return this.getLastBottomBlock(rootBlock);
    }

    /**
     * @param {BLOCK} thisBlock 
     */
    BlockContainer.prototype.getLastBottomBlock = function(thisBlock) {
        var childBlockList = thisBlock.getThisToLastBlockList();
        var childBlockList_down = childBlockList.filter(childBlock => {
            if (childBlock.getDirection() == BLOCK_DIRECTION.DOWN) {
                return true;
            } else {
                return false;
            }
        });
        if (childBlockList_down.length == 0) {
            return childBlockList[childBlockList.length-1];
        } else {
            return childBlockList_down[childBlockList_down.length-1];
        }
    }

    /** 블럭을 drag할 때 실핼하는 메소드
     * @param {boolean} isBlock true면 블럭의 이동, false면 Logic에 있는 블럭 생성 버튼의 이동
     * @param {Block} thisBlock
     * @param {Block} shadowBlock
     * @param {Block} selectedBlock   
     * @param {Direction} selectedBlockDirection
     * @param {number} currCursorX
     * @param {number} currCursorY
     */
    BlockContainer.prototype.dragBlock = function(isBlock, thisBlock, shadowBlock, selectedBlock, selectedBlockDirection, currCursorX, currCursorY) {
        var blockContainerThis = this;

        if (isBlock == true) {
            var nodeBlockList = blockContainerThis.getNodeBlockList();
            var lastBlockList_blockArea = []
            nodeBlockList.forEach(nodeBlock => {
                if (thisBlock.getUUID() == nodeBlock.getUUID()) {
                    return;
                }
                var lastBlock = nodeBlock.getLastBlock_from_nodeBlockArea();
                $( lastBlock.getBlockMainDom() ).css(STR_DISPLAY, STR_BLOCK);
                lastBlockList_blockArea.push(lastBlock);
            });
            // console.log('lastBlockList_blockArea',lastBlockList_blockArea);
        }

        /** 블록 전체를 돌면서 drag하는 Block과 Board위에 생성된 블록들과 충돌 작용  */
        var boardBlockList = blockContainerThis.getBlockList();
        boardBlockList.forEach( async (block) => {
            var blockType = block.getBlockType();
            if (blockType == BLOCK_CODELINE_TYPE.TEXT) {
                return;
            }

            if (isBlock == true) {
                /** 자기 자신인 블럭과는 충돌 금지 
                 *  혹은 자신의 하위 블럭과도 충돌 금지
                 */
                if ( thisBlock.getUUID() == block.getUUID()
                    || block.getIsNowMoved() == true ) {
                    return;
                }

                if (thisBlock.getBlockType() == BLOCK_CODELINE_TYPE.NODE) {
                    var isLastBlock = lastBlockList_blockArea.some(lastBlock => {
                        if (lastBlock.getUUID() == block.getUUID()) {
                            return true;
                        }
                    });

                    if (isLastBlock == false) {
                        return;
                    }
                }
            }

            /** 충돌할 block의 x,y, width, height를 가져온다 */
            var { x: blockX, 
                  y: blockY, 
                  width: blockWidth, 
                  height: blockHeight } = block.getBlockMainDomPosition();

            /** 블럭 충돌에서 벗어나는 로직 */
            var blockLeftHolderHeight = block.getBlockLeftHolderHeight();
            if ( (blockX > currCursorX 
                  || currCursorX > (blockX + blockWidth)
                  || blockY  > currCursorY 
                  || currCursorY > (blockY + blockHeight + blockHeight + blockHeight + blockLeftHolderHeight) ) ) {
                block.renderBlockHolderShadow(STR_NONE);
            }

            /** 블럭 충돌 left holder shadow 생성 로직 */
            if ( blockX < currCursorX
                && currCursorX < (blockX + blockWidth)
                && blockY  < currCursorY
                && currCursorY < (blockY + blockHeight + blockHeight + blockLeftHolderHeight) ) {     
                block.renderBlockHolderShadow(STR_BLOCK);
                block.renderBlockLeftHolderHeight();
            }

            /** 블럭 충돌 로직 */  
            if ( blockX < currCursorX
                    && currCursorX < (blockX + blockWidth + blockWidth)
                    && blockY  < currCursorY
                    && currCursorY < (blockY + blockHeight  + blockHeight) ) { 

                block.renderBlockLeftHolderHeight();

                /** 충돌시 direction 설정
                 * class, def, if, for, while, try, else, elif, finally, except Block은 INDENT
                 * 그 외 Block은 DOWN
                 */
                if ( IsCanHaveIndentBlock(blockType) ) {
                    selectedBlockDirection = BLOCK_DIRECTION.INDENT;
                } else {
                    selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                }
                shadowBlock.insertShadowDomToBlockDom( block, selectedBlockDirection);
    
            } else {

                selectedBlock = shadowBlock.getSelectBlock();

                var containerDom = blockContainerThis.getBlockContainerDom();
                var containerDomRect = $(containerDom)[0].getBoundingClientRect();
                var { x: containerDomX, 
                      y: containerDomY, 
                      width: containerDomWidth, 
                      height: containerDomHeight } = containerDomRect;
    
                /** board에 있는 어떠한 block에 닿았을 때 */
                if ( containerDomX < currCursorX
                     && currCursorX < (containerDomX + containerDomWidth)
                     && containerDomY  < currCursorY
                     && currCursorY < (containerDomY + containerDomHeight) ) {  
                    
                    /** board에 있는 어떠한 block에도 닿지 않았을 때 */
                } else {
                    /** shadow 블록 해제하는 로직
                     * css class로 마크된 block을 selectedBlock에 저장 한다
                     */
                    var $shadowBlockMainDom = $(shadowBlock.getBlockContainerDom());
     
                    $shadowBlockMainDom.css(STR_DISPLAY,STR_NONE);
                    shadowBlock.setSelectBlock(null);
                }
            }
        });

        return { 
            selectedBlock, 
            selectedBlockDirection
        };
    }

    /**
     * @param {boolean} isBlock true면 블럭의 이동, false면 Logic(Define, Control, Execute)에서 블럭의 생성
     * @param {Block} thisBlock 이동이 멈춘 블럭
     */
    BlockContainer.prototype.stopDragBlock = function(isBlock, thisBlock) {
        var blockContainerThis = this;

        /** 블록을 이동시킨 경우 */
        if (isBlock == true) {
            blockContainerThis.reRenderAllBlock();       
            thisBlock.renderEditorScrollTop();
        } else {
        /** 블록을 생성한 경우 */
            blockContainerThis.reRenderAllBlock_asc();
            blockContainerThis.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.BUTTONS);
        }

        /** 인자로 들어온 블럭의 node 블럭을 찾아 리턴 */
        var nodeBlock = blockContainerThis.findNodeBlock(thisBlock);
        nodeBlock.setIsNodeBlockToggled(false);
        $(nodeBlock.getBlockMainDom()).css(STR_BOX_SHADOW, STR_NONE);

        var childLowerDepthBlockList = nodeBlock.getBlockList_nodeBlockArea_noHolderBlock();
        childLowerDepthBlockList.forEach( block => {
            $(block.getBlockMainDom()).removeClass(VP_CLASS_STYLE_DISPLAY_NONE);
        });

        /** 
         *  모든 Block color 리셋
         */
        blockContainerThis.resetBlockList(thisBlock);
        var childLowerDepthBlockList = thisBlock.getBlockList_nodeBlockArea();
        childLowerDepthBlockList.forEach(block => {
            block.setIsNowMoved(false);
        });
    }

    /** 블럭 이동시 모든 블럭의 left holder height shadow 계산 */
    BlockContainer.prototype.reLoadBlockListLeftHolderHeight = function() {
        const blockContainerThis = this;
        const blockList = blockContainerThis.getBlockList();
        blockList.forEach(block => {
            const blockType = block.getBlockType();
            if ( IsCanHaveIndentBlock(blockType) == true ) {
                block.calculateLeftHolderHeightAndSet();
                const distance = block.getBlockLeftHolderHeight();
                $(block.getBlockLeftHolderDom()).css(STR_HEIGHT, distance);
            } 
        });
    }

    /**
     *  옵션 페이지를 새로 렌더링하는 메소드
     */
    BlockContainer.prototype.renderBlockOptionTab = function() {
        // console.log('renderBlockOptionTab');
        // console.log('selectedBlock',selectedBlock);
        var selectedBlock = this.getSelectBlock();
        if(selectedBlock) {
            selectedBlock.resetOptionPage();
            selectedBlock.renderOptionPage();
        }
    }

    /* 인자로 들어온 this 블럭이 속한 영역의 node 블럭을 찾아서 return */
    BlockContainer.prototype.findNodeBlock = function(thisBlock) {
        var blockContainerThis = this;
        var nodeBlockList = blockContainerThis.getNodeBlockList();
        var selectedBlock = blockContainerThis.getSelectBlock() || thisBlock;
        nodeBlockList.some(nodeBlock => {
            var childLowerDepthBlockList = nodeBlock.getBlockList_nodeBlockArea();
            childLowerDepthBlockList.push(nodeBlock);
            childLowerDepthBlockList.some(block => {
                if (block.getUUID() == selectedBlock.getUUID()) {
                    selectedBlock = nodeBlock;
                    return true;
                }
            });
        });
        return selectedBlock;
    }

    /**
     * @param {boolean} isAlone node 생성 할 때
     *                          true면 node 블럭 1개만 생성, (input에서 엔터 생성, +Node 블럭 생성의 경우)
     *                          false면 node 블럭의 자식으로 일반 블럭도 생성 (board에 어떤 블럭도 선택하지 않고 일반 블럭 생성할 경우)
     * @param {string} title node 블럭 이름
     */
    BlockContainer.prototype.createNodeBlock = function(isAlone = false, title = STR_EMPTY) {
        /** board에 블럭이 0개일 경우 */
        var isFirstBlock = false;
        const blockList = this.getBlockList();
        if (blockList.length == 0) {
            isFirstBlock = true;
        }

        var createdNodeBlock = this.createBlock(BLOCK_CODELINE_TYPE.NODE);

        var codeLineStr = STR_EMPTY;
        if (title) {
            codeLineStr = title;
        } else {
            var length = this.getNodeBlockNumber();
            codeLineStr = `Node ${length}`;
        }
        createdNodeBlock.setState({
            [STATE_codeLine]: codeLineStr
        });
        createdNodeBlock.setIsNodeBlockToggled(true);
        createdNodeBlock.writeCode(codeLineStr);

        /** 블럭 생성할 때,
         *  node 블럭 1개만 생성할 경우 
         */
        if (isAlone == true) {
            if (isFirstBlock == true) {
                createdNodeBlock.setDirection(BLOCK_DIRECTION.ROOT);
            } else {
                var lastBottomBlock = this.getRootToLastBottomBlock();
                lastBottomBlock.appendBlock(createdNodeBlock, BLOCK_DIRECTION.DOWN);
            }
            this.reRenderAllBlock_asc();
            this.resetBlockList(createdNodeBlock);
        }

        return createdNodeBlock;
    }

    BlockContainer.prototype.createTextBlock = function() {
        var isFirstBlock = false;
        const blockList = this.getBlockList();
        if (blockList.length == 0) {
            isFirstBlock = true;
        }

        const textBlockFuncID = 'com_markdown';
        var blockContainerThis = this;
        var createdBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.TEXT);
        createdBlock.setState({
            [STATE_codeLine]: STR_EMPTY
        });
        createdBlock.writeCode(STR_EMPTY);
        createdBlock.setFuncID(textBlockFuncID);
        createdBlock.setOptionPageLoadCallback(optionPageLoadCallback_block);
        createdBlock.setLoadOption(loadOption_block);

        if (isFirstBlock == true) {
            createdBlock.setDirection(BLOCK_DIRECTION.ROOT);
            this.reNewContainerDom();
        } else {
            const rootBlock = this.getRootBlock();
            const childBlockList = rootBlock.getThisToLastBlockList();
            childBlockList[childBlockList.length - 1].appendBlock(createdBlock, BLOCK_DIRECTION.DOWN);
        }
        this.reRenderAllBlock_asc(); 
        this.resetBlockList();
        this.setSelectBlock(createdBlock);
     

        setClosureBlock(createdBlock);
        loadOption_textBlock(textBlockFuncID, optionPageLoadCallback_block);
        createdBlock.renderSelectedBlockColor(false);
        return createdBlock;
    }

    /**
     * @param {string} funcID xml에 적힌 API List의 funcID
     * @param {string} naviInfo Common > Import 같은 naigation 정보
     */
    BlockContainer.prototype.createAPIListBlock = function(funcID, naviInfo) {
        this.resetBlockList();

        var isFirstBlock = false;
        const blockList = this.getBlockList();
        /** board에 블럭이 0개 일때
         *  즉 블럭이 처음으로 생성되는 경우
         */
        if (blockList.length == 0) {
            isFirstBlock = true;
        }

        var createdBlock_api = this.createBlock(BLOCK_CODELINE_TYPE.API);
        createdBlock_api.setFuncID(funcID);
        createdBlock_api.setOptionPageLoadCallback(optionPageLoadCallback_block);
        createdBlock_api.setLoadOption(loadOption_block);
        createdBlock_api.setState({
            [STATE_codeLine]: naviInfo
        });

        var thisBlock;
        var createdBlock_node;
        /** board에 블럭이 0개 있을 때 
         *  즉 블럭을 board에 처음 생성 할 때 
         */
        if (isFirstBlock == true) {
            createdBlock_node = this.createNodeBlock();
            this.reNewContainerDom();

            /** 최초 생성된 root 블럭 set root direction */
            createdBlock_node.setDirection(BLOCK_DIRECTION.ROOT);
            createdBlock_node.appendBlock(createdBlock_api, BLOCK_DIRECTION.DOWN);
            this.reRenderAllBlock_asc();

            const length = this.getNodeBlockNumber();
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_NODEBLOCK + createdBlock_node.getUUID()).html(`Node ${length}`);
            thisBlock = createdBlock_node;
        /**  board에 블럭이 1개 이상 있을 때 */
        } else {
            var selectedBlock = this.getSelectBlock();
            /** board에 선택한 블럭이 있고,
             *  선택한 블럭이 Text 블럭이 아닐 때
             */
            if (selectedBlock 
                && selectedBlock.getBlockType() != BLOCK_CODELINE_TYPE.TEXT) {
                        
                selectedBlock = this.findNodeBlock(selectedBlock);
                selectedBlock.getLastBlock_from_nodeBlockArea().appendBlock(createdBlock_api, BLOCK_DIRECTION.DOWN);
                selectedBlock.renderSelectedBlockColor(true);
                thisBlock = createdBlock_api;
                this.reRenderAllBlock_asc();
            /** 그 외의 경우 */
            } else {
                createdBlock_node = this.createNodeBlock();
                createdBlock_node.appendBlock(createdBlock_api, BLOCK_DIRECTION.DOWN);

                const nodeBlockAndTextBlockList = this.getNodeBlockAndTextBlockList_asc();
                nodeBlockAndTextBlockList[nodeBlockAndTextBlockList.length -1].getLastBlock_from_nodeBlockArea().appendBlock(createdBlock_node, BLOCK_DIRECTION.DOWN);
                thisBlock = createdBlock_node;
                    
                this.reRenderAllBlock_asc();

                const length = this.getNodeBlockNumber();
                    
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_NODEBLOCK + createdBlock_node.getUUID()).html(`Node ${length}`);
            }
        }

        /** sub 버튼 생성 */
        thisBlock.createSubButton();
        /** block color 색칠 */
        thisBlock.renderMyColor(true);

        createdBlock_api.writeCode(naviInfo);
        setClosureBlock(createdBlock_api);
        loadOption_block(funcID, optionPageLoadCallback_block);
    }

    /** 블럭을 이동할 때,
     *  shadow 블럭을 만드는 메소드
     * @param {ENUM} blockType 
     * @param {Block} thisBlock 
     */
    BlockContainer.prototype.createShadowBlock = function( blockType, thisBlock) {
        var blockContainerThis = this;
        var shadowBlock = new ShadowBlock(blockContainerThis, blockType, thisBlock);
        var $shadowBlockContainerDom = $(shadowBlock.getBlockContainerDom());
        $shadowBlockContainerDom.css(STR_DISPLAY, STR_NONE);

        var containerDom = blockContainerThis.getBlockContainerDom();
        $(containerDom).append(shadowBlock.getBlockContainerDom());

        return shadowBlock;
    }

    /** board에 container dom을 새로 만드는 메소드 */
    BlockContainer.prototype.reNewContainerDom = function() {
        // console.log('reNewContainerDom');
        // var blockContainerThis = this;
     
        /** 기존의 block container dom 삭제 */
        var containerDom = this.getBlockContainerDom();
        $(containerDom).empty();
        $(containerDom).remove();
        $(VP_CLASS_PREFIX + VP_CLASS_BLOCK_CONTAINER).remove();

        /** 새로운 block container dom 생성 */
        var containerDom = document.createElement(STR_DIV);
        containerDom.classList.add(VP_CLASS_BLOCK_CONTAINER);

        $(containerDom).css(STR_TOP, NUM_DEFAULT_POS_Y + STR_PX);
        $(containerDom).css(STR_LEFT, NUM_DEFAULT_POS_X + STR_PX);

        /** +Node, +Text 버튼 생성 */
        var sbNodeOrTextPlusButton = new sb.StringBuilder();
        sbNodeOrTextPlusButton.appendFormatLine("<div id='{0}' class='{1}'>",'vp_apiblock_board_node_plus_button_container',
                                                                            'vp-apiblock-style-flex-row');
        sbNodeOrTextPlusButton.appendFormatLine("<div id='{0}' class='{1}'>",'vp_apiblock_board_node_plus_button',
                                                                            'vp-apiblock-option-plus-button');
        sbNodeOrTextPlusButton.appendFormatLine("{0}", '+ Node');
        sbNodeOrTextPlusButton.appendLine("</div>");

        sbNodeOrTextPlusButton.appendFormatLine("<div id='{0}' class='{1}' style='{2}'>",'vp_apiblock_board_text_plus_button',
                                                                                         'vp-apiblock-option-plus-button',
                                                                                         'margin-left: 10px');
        sbNodeOrTextPlusButton.appendFormatLine("{0}", '+ Text');
        sbNodeOrTextPlusButton.appendLine("</div>");

        sbNodeOrTextPlusButton.appendLine("</div>");
        var nodePlusButtonContainer = sbNodeOrTextPlusButton.toString();

        $(containerDom).append(nodePlusButtonContainer);

        $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).append(containerDom);
        this.setBlockContainerDom(containerDom);

        return containerDom;
    }
    
    
    /** Block의 HTML 생성
     *  @param {Block} thisBlock
     *  @param {boolean} isFirst 
    */
    BlockContainer.prototype.makeBlockDom = function(thisBlock, isFirst) {
        /** 이동하는 block과 동일한 모양의 html tag 생성*/
        var blockMainDom = document.createElement(STR_DIV);
        blockMainDom.classList.add('vp-block');
        blockMainDom.classList.add(`vp-block-${thisBlock.getUUID()}`);

        var blockType = thisBlock.getBlockType()
        if (blockType == BLOCK_CODELINE_TYPE.NODE
            || blockType == BLOCK_CODELINE_TYPE.TEXT) {

            if (blockType == BLOCK_CODELINE_TYPE.NODE) {
                $(blockMainDom).css(STR_BACKGROUND_COLOR, STR_TRANSPARENT);
            }
            
            $(blockMainDom).css('margin-top', NUM_NODE_OR_TEXT_BLOCK_MARGIN_TOP_PX);
        } else if (blockType == BLOCK_CODELINE_TYPE.HOLDER) {
            blockMainDom.classList.add(VP_CLASS_BLOCK_BOTTOM_HOLDER);
        } 

        /** 이동하는 block의 header 생성 */
 
        var classOrDefName;
        /** class */
        if ( blockType == BLOCK_CODELINE_TYPE.CLASS ) {
            classOrDefName = thisBlock.getState(STATE_className);
        /** def 이름 */
        } else if ( blockType == BLOCK_CODELINE_TYPE.DEF ) {
            classOrDefName = thisBlock.getState(STATE_defName);
        }
        
        var codeLineStr = '';
        if ( blockType == BLOCK_CODELINE_TYPE.CLASS ) {
            codeLineStr = GenerateClassInParamList(thisBlock);
        } else if ( blockType == BLOCK_CODELINE_TYPE.DEF ) {
            codeLineStr = GenerateDefInParamList(thisBlock);
        } else if (blockType == BLOCK_CODELINE_TYPE.IF) {
            codeLineStr = GenerateIfConditionList(thisBlock, BLOCK_CODELINE_TYPE.IF);
        } else if (blockType == BLOCK_CODELINE_TYPE.ELIF) {
            codeLineStr = GenerateIfConditionList(thisBlock, BLOCK_CODELINE_TYPE.ELIF);
        } else if (blockType == BLOCK_CODELINE_TYPE.FOR) {
            codeLineStr = GenerateForParam(thisBlock);
        } else if (blockType == BLOCK_CODELINE_TYPE.WHILE) {
            codeLineStr = GenerateWhileConditionList(thisBlock);
        } else if (blockType == BLOCK_CODELINE_TYPE.EXCEPT) {
            codeLineStr = GenerateExceptConditionList(thisBlock);
        } else if (blockType == BLOCK_CODELINE_TYPE.RETURN) {
            codeLineStr = GenerateReturnOutParamList(thisBlock);
        } else if (blockType == BLOCK_CODELINE_TYPE.LAMBDA) {
            codeLineStr = GenerateLambdaParamList(thisBlock);
        } else if (blockType == BLOCK_CODELINE_TYPE.IMPORT) {
            codeLineStr = ShowImportListAtBlock(thisBlock);
        } else if ( blockType == BLOCK_CODELINE_TYPE.API ) {
            codeLineStr = thisBlock.getState(STATE_codeLine)
        } else if (                           
            blockType == BLOCK_CODELINE_TYPE.BREAK  
            || blockType == BLOCK_CODELINE_TYPE.CONTINUE  
            || blockType == BLOCK_CODELINE_TYPE.PASS 
            || blockType == BLOCK_CODELINE_TYPE.CODE  
            || blockType == BLOCK_CODELINE_TYPE.COMMENT 
            || blockType == BLOCK_CODELINE_TYPE.PRINT
            || blockType == BLOCK_CODELINE_TYPE.PROPERTY
            || blockType == BLOCK_CODELINE_TYPE.TEXT) {
            codeLineStr = thisBlock.getState(STATE_codeLine);
        } else if (blockType == BLOCK_CODELINE_TYPE.NODE) {
            codeLineStr = thisBlock.getState(STATE_codeLine);
        }

        var blockName = thisBlock.getBlockName();
        if ( blockType == BLOCK_CODELINE_TYPE.CODE
            || blockType == BLOCK_CODELINE_TYPE.PASS
            || blockType == BLOCK_CODELINE_TYPE.CONTINUE 
            || blockType == BLOCK_CODELINE_TYPE.BREAK
            || blockType == BLOCK_CODELINE_TYPE.LAMBDA
            || blockType == BLOCK_CODELINE_TYPE.NODE
            || blockType == BLOCK_CODELINE_TYPE.TEXT
            || blockType == BLOCK_CODELINE_TYPE.API ) {
            blockName = '';
        } else if (blockType == BLOCK_CODELINE_TYPE.PROPERTY) {
            blockName = '@';
        } else if (blockType == BLOCK_CODELINE_TYPE.COMMENT) {
            blockName = '#';
        }

        var sbMainHeader = new sb.StringBuilder();
        var blockUUID = thisBlock.getUUID();
        if (blockType == BLOCK_CODELINE_TYPE.NODE) {
            sbMainHeader.appendFormatLine("<div class='{0}' style='{1}'>",'vp-block-header', 'padding-left: 0rem;');
            sbMainHeader.appendFormatLine("<div class='{0}' style='{1}'>",  'vp-apiblock-codeline-ellipsis',
                                                                            'background-color:white; margin-left: 0em; margin-right: 0em;');

            sbMainHeader.appendFormatLine("<div class='{0}'>",'vp-apiblock-nodeblock');

            sbMainHeader.appendFormatLine("<div class='{0} {1} {2}'>",`vp-block-header-param`, 
                                                                      `vp-block-header-${blockUUID}`,
                                                                      `vp-apiblock-nodeblock${blockUUID}`);

            sbMainHeader.appendFormatLine("<div class='{0}'>",'vp-apiblock-nodeblock-text');
            sbMainHeader.appendFormatLine("{0}", codeLineStr);

            sbMainHeader.appendLine("</div>");

            sbMainHeader.appendLine("</div>");

            sbMainHeader.appendFormatLine("<input id='{0}' class='{1} {2}' style='{3}' value='{4}'/>", 
                                                                            `vp_apiblock_nodeblock_input_${blockUUID}`,
                                                                            'vp-apiblock-nodeblock-input',
                                                                            `vp-apiblock-nodeblock-input${blockUUID}`,
                                                                            'display:none',
                                                                             codeLineStr);

            sbMainHeader.appendLine("</div>");
            sbMainHeader.appendLine("</div>");
            sbMainHeader.appendLine("</div>");
  
   
        } else if (blockType == BLOCK_CODELINE_TYPE.CLASS   
                    || blockType == BLOCK_CODELINE_TYPE.DEF) {
            sbMainHeader.appendFormatLine("<div class='{0}'>",'vp-block-header');

            sbMainHeader.appendFormatLine("<strong class='{0}' style='margin-right:10px;'>",'vp-block-header-name');
            sbMainHeader.appendFormatLine("{0}", blockName);
            sbMainHeader.appendLine("</strong>");

            sbMainHeader.appendFormatLine("<div class='{0}'>",'vp-apiblock-codeline-ellipsis');
            sbMainHeader.appendFormatLine("<div class='{0}'>",'vp-apiblock-style-flex-row');

            sbMainHeader.appendFormatLine("<div class='{0} {1}' style='{2}'>", `vp-block-header-class-name-${blockUUID}`, 
                                                                               `vp-block-header-def-name-${blockUUID}`,
                                                                               'font-size:12px');
            sbMainHeader.appendFormatLine("{0}", classOrDefName);
            sbMainHeader.appendLine("</div>");

            sbMainHeader.appendFormatLine("<div class='{0} {1}' style='{2}'>", `vp-block-header-param`, 
                                                                                `vp-block-header-${blockUUID}`,
                                                                                'text-indent: 0em');
            sbMainHeader.appendFormatLine("{0}", codeLineStr);
            sbMainHeader.appendLine("</div>");

            sbMainHeader.appendLine("</div>");
            sbMainHeader.appendLine("</div>");

            sbMainHeader.appendLine("</div>");

        
        } else if (blockType == BLOCK_CODELINE_TYPE.IF    
                    || blockType == BLOCK_CODELINE_TYPE.FOR 
                    || blockType == BLOCK_CODELINE_TYPE.TRY 
                    || blockType == BLOCK_CODELINE_TYPE.ELIF
                    || blockType == BLOCK_CODELINE_TYPE.WHILE 
                    || blockType == BLOCK_CODELINE_TYPE.EXCEPT
                    || blockType == BLOCK_CODELINE_TYPE.RETURN  
                    || blockType == BLOCK_CODELINE_TYPE.LAMBDA 
                    || blockType == BLOCK_CODELINE_TYPE.IMPORT 
                    || blockType == BLOCK_CODELINE_TYPE.API

                    || blockType == BLOCK_CODELINE_TYPE.ELSE
                    || blockType == BLOCK_CODELINE_TYPE.FINALLY

                    || blockType == BLOCK_CODELINE_TYPE.BREAK  
                    || blockType == BLOCK_CODELINE_TYPE.CONTINUE  
                    || blockType == BLOCK_CODELINE_TYPE.PASS 
                    || blockType == BLOCK_CODELINE_TYPE.CODE  
                    || blockType == BLOCK_CODELINE_TYPE.COMMENT 
                    || blockType == BLOCK_CODELINE_TYPE.PRINT
                    || blockType == BLOCK_CODELINE_TYPE.PROPERTY
                    || blockType == BLOCK_CODELINE_TYPE.TEXT ) {

            sbMainHeader.appendFormatLine("<div class='{0}' style='{1}'>", 'vp-block-header', blockType == BLOCK_CODELINE_TYPE.TEXT
                                                                                                    ? 'height: unset;'
                                                                                                    : '');
            if ( blockType == BLOCK_CODELINE_TYPE.BREAK  
                || blockType == BLOCK_CODELINE_TYPE.CONTINUE  
                || blockType == BLOCK_CODELINE_TYPE.PASS 
                || blockType == BLOCK_CODELINE_TYPE.CODE  
                || blockType == BLOCK_CODELINE_TYPE.COMMENT
                || blockType == BLOCK_CODELINE_TYPE.PROPERTY
                || blockType == BLOCK_CODELINE_TYPE.API
                || blockType == BLOCK_CODELINE_TYPE.LAMBDA ) {
                sbMainHeader.appendFormatLine("<strong class='{0}'>",'vp-block-header-name');
                sbMainHeader.appendFormatLine("{0}", blockName);
                sbMainHeader.appendLine("</strong>");
            } else {
                sbMainHeader.appendFormatLine("<strong class='{0}' style='margin-right:10px;'>",'vp-block-header-name');
                sbMainHeader.appendFormatLine("{0}", blockName);
                sbMainHeader.appendLine("</strong>");
            }

            sbMainHeader.appendFormatLine("<div class='{0}'>",'vp-apiblock-codeline-ellipsis');

            sbMainHeader.appendFormatLine("<div class='{0} {1}'>",'vp-block-header-param', `vp-block-header-${blockUUID}`);
            sbMainHeader.appendFormatLine("{0}", codeLineStr);
            sbMainHeader.appendLine("</div>");

            sbMainHeader.appendLine("</div>");

            sbMainHeader.appendLine("</div>");
        }

        const mainHeaderDom = $(sbMainHeader.toString());
        $(blockMainDom).append(mainHeaderDom);
        blockMainDom = RenderHTMLDomColor(thisBlock, blockMainDom);

        var blockLeftHolderDom = document.createElement(STR_DIV);
        blockLeftHolderDom.classList.add('vp-block-left-holder');
        const blockLeftHolderHeight = thisBlock.getBlockLeftHolderHeight();
        $(blockLeftHolderDom).css(STR_HEIGHT, blockLeftHolderHeight + STR_PX);
        $(blockMainDom).append(blockLeftHolderDom);

        if (isFirst == false) {
            /** 이동하는 block의 처음 block의 width 값 계산 */
            const rect = thisBlock.getBlockMainDomPosition();
            $(blockMainDom).css(STR_WIDTH, rect.width);
        } 

        var blockDepthInfoDom = $(`<span class='vp-block-depth-info'></span>`);
        var isShowDepth = this.getIsShowDepth();
        if ( isShowDepth == false ) {
            $(blockDepthInfoDom).css(STR_OPACITY, 0);
        }
        
        $(blockMainDom).append(blockDepthInfoDom);

        if (blockType == BLOCK_CODELINE_TYPE.TEXT) {
            $(blockMainDom).css(STR_BACKGROUND_COLOR, STR_TRANSPARENT);
            $(blockMainDom).css(STR_WIDTH, NUM_TEXT_BLOCK_WIDTH);
        } else {
            var blockMaxWidth = this.getBlockMaxWidth() - (thisBlock.getDepth() * NUM_INDENT_DEPTH_PX);
            $(blockMainDom).css(STR_WIDTH, blockMaxWidth);
        }

        return blockMainDom;
    }

    BlockContainer.prototype.makeShadowBlockDom = function(thisBlock) {
        var sbBlockMainDom = new sb.StringBuilder();
        sbBlockMainDom.appendFormatLine("<div class='{0}' style='{1}'>", VP_BLOCK, 'width=100%;');

        sbBlockMainDom.appendFormatLine("<div class='{0}'>",'vp-block-inner');
        sbBlockMainDom.appendFormatLine("<div class='{0}'>",'vp-block-header');
        sbBlockMainDom.appendFormatLine("<strong class='{0}' style='{1}'>",'vp-apiblock-style-flex-column-center',`margin-right:10px; 
                                                                                                    font-size:12px; 
                                                                                                    color: #252525;`);
        sbBlockMainDom.appendFormatLine("{0}",thisBlock.getBlockName());
        sbBlockMainDom.appendLine("</strong>");
        sbBlockMainDom.appendLine("</div>");
        sbBlockMainDom.appendLine("</div>");

        sbBlockMainDom.appendLine("</div>");

        var blockMainDom = $(sbBlockMainDom.toString());
        blockMainDom = RenderHTMLDomColor(thisBlock, blockMainDom);
        $(blockMainDom).css(STR_OPACITY, NUM_SHADOWBLOCK_OPACITY);

        var blockType = thisBlock.getBlockType()
        if (blockType == BLOCK_CODELINE_TYPE.HOLDER) {
            $(blockMainDom).addClass(VP_CLASS_BLOCK_BOTTOM_HOLDER);
        } 

        return blockMainDom;
    }

    BlockContainer.prototype.makeBlockLineNumberInfoDom = function(block) {
        var sbBlockLineNumberInfoDom = new sb.StringBuilder();
        sbBlockLineNumberInfoDom.appendFormatLine("<span class='{0}'>", VP_CLASS_BLOCK_NUM_INFO);
        sbBlockLineNumberInfoDom.appendFormatLine("<span class='{0}'>", 'vp-block-prefixnum-info');
        sbBlockLineNumberInfoDom.appendLine("</span>");

        sbBlockLineNumberInfoDom.appendFormatLine("<span class='{0}'>", 'vp-block-linenumber-info');
        sbBlockLineNumberInfoDom.appendLine("</span>");

        sbBlockLineNumberInfoDom.appendLine("</span>");

        var blockMainDom = block.getBlockMainDom();
        $(blockMainDom).append(sbBlockLineNumberInfoDom.toString());

        return blockMainDom;
    }

    /** 
     *  Block List들의 color를 리셋하고 인자로 받은 block의  
     *  1. 옵션 팝업을 열고, 2. sub 버튼을 생성하고, 3. color를 색칠
     * @param {Block} thisBlock 
     */ 
    BlockContainer.prototype.resetBlockList = function(thisBlock) {

        /** 전체 블럭 리스트 리셋*/
        const blockList = this.getBlockList();
        blockList.forEach(block => {
            block.renderBlockHolderShadow(STR_NONE);
            block.renderSelectedBlockColor(false);
            $(block.getBlockMainDom()).css(STR_BORDER, '2px solid transparent');
            $(block.getBlockMainDom()).find(VP_CLASS_PREFIX + VP_CLASS_BLOCK_SUB_BTN_CONTAINER).remove();
        });
        
        /** node 블럭 리스트 리셋 */
        const nodeBlockList = this.getNodeBlockList();
        /** node 블럭이 input 태그 상태라면 일반 상태로 변경 */
        nodeBlockList.forEach(nodeBlock => {
            nodeBlock.setNodeBlockInput(STR_NONE);
        });

        if (thisBlock) {
            this.setSelectBlock(thisBlock);
            /** 옵션 페이지 다시 오픈 */
            this.renderBlockOptionTab(thisBlock);
            /** 서브 버튼 생성 */
            thisBlock.createSubButton();
            /** 자식 하위 Depth Block Border 색칠 */
            thisBlock.renderMyColor(true);
        }
    }

    /** importPackage의 generateCode 이전에 실행할 prefix code
     *  @param {boolean} isClicked true면 클릭 이벤트로 코드 실행
     */
    BlockContainer.prototype.generateCode = function(isClicked) {
        var importPackageThis = this.getImportPackageThis();
        importPackageThis.generateCode(true, true, isClicked);
    }

    /** 코드 생성 */
    BlockContainer.prototype.makeCode = function(thisBlock) {
        var codeLine = '';
        var childLowerDepthBlockList = thisBlock.getBlockList_nodeBlockArea_noHolderBlock();
        var rootDepth = thisBlock.getDepth();
        childLowerDepthBlockList.some( ( block,index ) => {
            var indentString = block.getIndentString(rootDepth);
            if ( block.getBlockType() == BLOCK_CODELINE_TYPE.API ) {
                var apiCodeLine = block.setCodeLineAndGet(indentString, true);
                if (apiCodeLine.indexOf('BREAK_RUN') != -1 || apiCodeLine == '') {
                    codeLine = 'BREAK_RUN';
                    return true;
                } else {
                    codeLine += apiCodeLine;
                }
            } else {
                codeLine += block.setCodeLineAndGet(indentString, false);
            }
            codeLine += STR_KEYWORD_NEW_LINE;
        });
        vpCommon.setIsAPIListRunCode(true);
        return codeLine;
    }

    /** Run All 버튼 실행시 board에 있는 전체 코드 생성 */
    BlockContainer.prototype.makeAllCode = function() {
        var rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return;
        }

        // var isBreakRun = false;
        var codeLineStr = STR_EMPTY;
        var blockList = rootBlock.getRootToChildBlockList();
        var rootDepth = rootBlock.getDepth();
        blockList.some( (block,index) => {

            if (block.getBlockType() == BLOCK_CODELINE_TYPE.HOLDER) {
                return;
            }
            /** 각 Block의 blockCodeLine에 맞는 코드 생성 */
            var indentString = block.getIndentString(rootDepth);
            var codeLine = STR_EMPTY;
            if ( block.getBlockType() == BLOCK_CODELINE_TYPE.API ) {
                var apiCodeLine = block.setCodeLineAndGet(indentString, true);
                if (apiCodeLine.indexOf('BREAK_RUN') != -1 || apiCodeLine == '') {
                    codeLineStr += 'BREAK_RUN';
                    // isBreakRun = true;
                    return true;
                } else {
                    codeLine += apiCodeLine;
                }
            } else {
                codeLine += block.setCodeLineAndGet(indentString, false);
            }

            /**  코드 라인 한 칸 띄우기 */    
            codeLine += STR_KEYWORD_NEW_LINE;
            codeLineStr += codeLine;
        });

        this.setAPIBlockCode(codeLineStr);
        return codeLineStr;
    }

    /** text 블럭 코드 실행 */
    BlockContainer.prototype.makeCode_textBlock = function(thisBlock) {
        thisBlock.getImportPakage().generateCode(true, true);
    }

    /** node 블럭 클릭할 때 preview */
    BlockContainer.prototype.previewCode = function(thisBlock) {
        vpCommon.setIsAPIListRunCode(false);

        var rootDepth = thisBlock.getDepth();
        var codeLine = ``;
        var childLowerDepthBlockList = thisBlock.getBlockList_nodeBlockArea_noHolderBlock();
        childLowerDepthBlockList.forEach( ( block ) => {
            var indentString = block.getIndentString(rootDepth);
            var thisCodeLine =  block.setCodeLineAndGet(indentString, false);
            /** api list validation 걸릴 때 BREAK_RUN을 반환*/
            if (thisCodeLine.indexOf('BREAK_RUN') != -1) {
                /** 그래서 BREAK_RUN을 replace함수로 제거 */
                thisCodeLine = thisCodeLine.replace('BREAK_RUN','');
            }
            codeLine += thisCodeLine;
            codeLine += STR_KEYWORD_NEW_LINE;
        });

        vpCommon.setIsAPIListRunCode(true);
        return codeLine;
    }

    /**
     * block의 depth를 계산하고 block 앞에 depth 를 보여주는 함수
     */
    BlockContainer.prototype.calculateDepthAndSetDepth = function() {
        const rootBlock = this.getRootBlock();
        if (rootBlock) {
            const childBlockList = rootBlock.getThisToLastBlockList();
            childBlockList.forEach((block) => {
                var depth = block.calculateDepthAndGet();
                var blockDepthInfoDom = block.getBlockDepthInfoDom();
                blockDepthInfoDom.text(depth);
            });
        }
    }



    /** API Block 전체를 resize  할 때 */
    BlockContainer.prototype.resizeAPIblock = function() {
        var mainPageRectWidth = $(VP_ID_PREFIX + VP_ID_WRAPPER).css(STR_WIDTH);
        var index = mainPageRectWidth.indexOf('px');
        var mainPageRectWidthNum = parseInt(mainPageRectWidth.slice(0,index));

        var buttonsPageRectWidth = NUM_BUTTONS_PAGE_WIDTH; 
        var boardPageRect =  $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD_CONTAINER))[0].getBoundingClientRect(); 
        var boardPageRectWidth = boardPageRect.width;
        var optionPageRectWidth = mainPageRectWidthNum - boardPageRectWidth - buttonsPageRectWidth - 103;

        if (optionPageRectWidth < NUM_OPTION_PAGE_WIDTH) {
            boardPageRectWidth = mainPageRectWidthNum - NUM_OPTION_PAGE_WIDTH - 103 - buttonsPageRectWidth;
        } 

        var optionPageRectWidth_maxWidth = mainPageRectWidthNum - buttonsPageRectWidth - NUM_API_BOARD_CENTER_PAGE_MIN_WIDTH - 103;
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_MAX_WIDTH, optionPageRectWidth_maxWidth);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD_CONTAINER)).css(STR_WIDTH, boardPageRectWidth );
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, optionPageRectWidth );
        $(VP_ID_PREFIX + VP_ID_WRAPPER).css(STR_MIN_WIDTH, 760);
        // min-width: 930px 
        this.setOptionPageWidth(optionPageRectWidth);
        this.setBlockMaxWidth_blockList(boardPageRectWidth);
    }

    /** option popup을 resize  할 때 */
    BlockContainer.prototype.resizeOptionPopup = function() {
        // console.log('resizeOptionPopup');

        var optionPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB))[0].getBoundingClientRect();
        var mainPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MAIN))[0].getBoundingClientRect();
        var buttonsPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS))[0].getBoundingClientRect();
        
        var mainPageRectWidth = mainPageRect.width; 
        var buttonsPageRectWidth = buttonsPageRect.width; 
        var optionPageRectWidth = optionPageRect.width;
        var boardPageRectWidth = mainPageRectWidth - optionPageRectWidth - buttonsPageRectWidth - 10;

        if (boardPageRectWidth > NUM_API_BOARD_CENTER_PAGE_MIN_WIDTH) {
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_MAX_WIDTH, 'unset !important;');
        } else {
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_MAX_WIDTH, optionPageRectWidth);
        }

        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD_CONTAINER)).css(STR_WIDTH, boardPageRectWidth );
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, optionPageRectWidth);
        
        this.setOptionPageWidth(optionPageRectWidth); 
        this.setBlockMaxWidth_blockList(boardPageRectWidth);

        this.setBlockMaxWidth(boardPageRectWidth - 70);
    }
    
    /** resize할 때
     *  board의 width를 토대로 블럭의 max width를 정하고
     *  max width를 토대로 블럭의 width를 다시 표시함
     */
    BlockContainer.prototype.setBlockMaxWidth_blockList = function(boardPageRectWidth) {
        var blockList = this.getBlockList();
        blockList.forEach(block => {
            var blockMaxWidth = boardPageRectWidth - 70;
            this.setBlockMaxWidth(blockMaxWidth);

            var indentDepthNum = block.getIndentNumber();
            var blockWidth = blockMaxWidth - indentDepthNum;
            var blockMainDom = block.getBlockMainDom();
            $(blockMainDom).css(STR_WIDTH, blockWidth);
        });
    }


    /**  LoadedVariableList  예제
        0:
        varName: "cam"
        varType: "DataFrame"
    */
    BlockContainer.prototype.setKernelLoadedVariableList = function(loadedVariableList) {
        this.loadedVariableList = loadedVariableList;
    }

    /** varName varType를 Array로 다 가져오기*/
    BlockContainer.prototype.getKernelLoadedVariableList = function() {
        return this.loadedVariableList;
    }

    /** varName만 Array로 가져오기*/
    BlockContainer.prototype.getKernelLoadedVariableNameList = function() {
        return this.loadedVariableList.map(varData => {
            return varData.varName;
        });
    }

    /** metadata init */
    BlockContainer.prototype.setAPIBlockMetadataHandler = function() {  
        var importPackageThis = this.getImportPackageThis();
        this.setMetahandler(importPackageThis.funcID);
        this.mdHandler.generateMetadata(importPackageThis);  
        this.mdHandler.metadata.apiblockList = [];
    }

    /** metadata set */
    BlockContainer.prototype.setAPIBlockMetadata = function() {  
        var importPackageThis = this.getImportPackageThis();  
        var apiBlockJsonDataList = this.makeAPIBlockMetadata();  
        var encoded_apiBlockJsonDataList = encodeURIComponent(JSON.stringify(apiBlockJsonDataList));
        
        /** API BLOCK container가 가지고 있는 metadata 
         *  이 데이터는 API Block가 metadata를 핸들링하기 위해 존재
         */
        this.mdHandler.metadata.apiblockList = encoded_apiBlockJsonDataList;
        /** importPackage가 가지고 있는 metadata 
         *  이 데이터는 #vp_saveOn 버튼을 누를시 vpNote로 간다.
        */
        importPackageThis.metadata = this.mdHandler.metadata;        
    }

    /** metadata 로드 */
    BlockContainer.prototype.loadAPIBlockMetadata = function(loadedMetadata) {
        if (loadedMetadata) {
            var importPackageThis = this.getImportPackageThis(); 
            var decodedMetadata = decodeURIComponent(loadedMetadata.apiblockList);
            var parsedDecodedMetadata = JSON.parse(decodedMetadata);

            this.mdHandler.metadata = loadedMetadata;
            this.mdHandler.metadata.apiblockList = parsedDecodedMetadata;
            importPackageThis.metadata = this.mdHandler.metadata;  

            this.reRenderBlockList_fromMetadata(parsedDecodedMetadata);   
        } 
    }

    /** metadata 세이브 */
    BlockContainer.prototype.saveAPIBlockMetadata = function() {  
        var apiBlockJsonDataList = this.makeAPIBlockMetadata();  
        var importPackageThis = this.getImportPackageThis();  
        var encoded_apiBlockJsonDataList = encodeURIComponent(JSON.stringify(apiBlockJsonDataList));
        this.mdHandler.metadata.apiblockList = encoded_apiBlockJsonDataList;

        importPackageThis.metadata = this.mdHandler.metadata;  
        this.mdHandler.saveMetadata(this.mdHandler.metadata);
    }


    /** ---------------------option popup dom 관련 메소드 --------------------------------------- */
    //
    BlockContainer.prototype.setOptionDom = function(UUID, type, blockOptionPageDom_new) {
        this.setOptionDomPool_none();
        // console.log('setOptionDom');
        if (this.domPool.get(UUID)) {
            if (type == BLOCK_CODELINE_TYPE.TEXT || type == BLOCK_CODELINE_TYPE.API) {
                const blockOptionPageDom_old = this.domPool.get(UUID);
                $(blockOptionPageDom_old).css(STR_DISPLAY, STR_NONE);
            } else {
                const blockOptionPageDom_old = this.domPool.get(UUID);
                $(blockOptionPageDom_old).remove();
            }
        }
        this.domPool.set(UUID, blockOptionPageDom_new);
        $('.vp-apiblock-option-tab-none').css(STR_DISPLAY, STR_NONE);
    }

    BlockContainer.prototype.getOptionDom = function(UUID) {
        const blockOptionPageDom = this.domPool.get(UUID);
        return blockOptionPageDom;
    }

    BlockContainer.prototype.deleteOptionDom = function(UUID) {
        if (this.domPool.get(UUID)) {
            const blockOptionPageDom_old = this.domPool.get(UUID);
            $(blockOptionPageDom_old).css({
                display: STR_NONE
            });
        }
    }
    BlockContainer.prototype.removeOptionDom = function(UUID) {
        if (this.domPool.get(UUID)) {
            const blockOptionPageDom_old = this.domPool.get(UUID);
            $(blockOptionPageDom_old).remove();
        }
    }
    BlockContainer.prototype.deleteAllOptionDom = function() {
        this.domPool.clear();

        var optionPageSelector = this.getOptionPageSelector();
        $(optionPageSelector + ' .vp-apiblock-option').remove();
        $(optionPageSelector + ' .vp-option-page').remove();
    }

    BlockContainer.prototype.reRenderOptionDomPool = function(blockOptionPageDom_new) {
        for (const blockOptionPageDom_old of this.domPool.values()) {
            $(blockOptionPageDom_old).css({
                display: STR_NONE
            });
        }
        $(blockOptionPageDom_new).css({
            display: STR_BLOCK
        });
    }

    /** 옵션 페이지에 있는 옵션 페이지들 전부 none 처리 */
    BlockContainer.prototype.setOptionDomPool_none = function() {
        for (const blockOptionPageDom_old of this.domPool.values()) {
            $(blockOptionPageDom_old).css(STR_DISPLAY, STR_NONE);
        }

        var optionPageSelector = this.getOptionPageSelector();
        $(optionPageSelector + ' .vp-apiblock-option').css(STR_DISPLAY, STR_NONE);
        $(optionPageSelector + ' .vp-option-page').css(STR_DISPLAY, STR_NONE);
    }

    /** 옵션페이지를  (N/A)로 표기 */
    BlockContainer.prototype.resetOptionPage = function() {
        this.setOptionDomPool_none();
        $('.vp-apiblock-option-tab-none').css(STR_DISPLAY, STR_BLOCK);
        this.setSelectBlock(null);
    }

    BlockContainer.prototype.getBoardPage_$ = function() {
        var $boardPage = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD));
        return $boardPage;
    }

    BlockContainer.prototype.getOptionPage_$ = function() {
        var $optionPage = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB_SELECTOR));
        return $optionPage;
    }

    BlockContainer.prototype.getOptionPageSelector = function() {
        var optionPageSelector = VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB_SELECTOR;
        return optionPageSelector;
    }
    return BlockContainer;
});
