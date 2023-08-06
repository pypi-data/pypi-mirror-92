define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'

    , './api.js'    

    , './constData.js'
    , './blockContainer.js'
    , './createBlockBtn.js'
    , './createApiBtn.js'
    , './createGroup.js'
    , './api_list.js'

    , './component/boardMenuBar.js'
], function ( $, vpCommon, vpConst, 
              api, constData, blockContainer, createBlockBtn, createApiBtn, createGroup, api_list,
              apiBlockMenuInit ) {
 
    const { ControlToggleInput, LoadVariableList, MapGroupTypeToName } = api;
  
    const { BLOCK_GROUP_TYPE
            , BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , FOCUSED_PAGE_TYPE
            , BLOCK_DIRECTION

            , VP_ID_PREFIX
            , VP_ID_WRAPPER
            , VP_ID_APIBLOCK_LEFT_TAB_API
            , VP_ID_APIBLOCK_LEFT_TAP_APILIST_PAGE
            , VP_ID_APIBLOCK_NODE_BLOCK_PLUS_BUTTON
            , VP_ID_APIBLOCK_TEXT_BLOCK_PLUS_BUTTON
            , VP_ID_APIBLOCK_BOARD_MAKE_NODE_BLOCK_INPUT 

            , VP_CLASS_PREFIX
            , VP_CLASS_BLOCK_GROUPBOX_PREFIX
            , VP_CLASS_APIBLOCK_MAIN
            , VP_CLASS_APIBLOCK_BODY
            , VP_CLASS_APIBLOCK_BOARD_CONTAINER
            , VP_CLASS_APIBLOCK_MENU_BTN
            , VP_CLASS_MAIN_CONTAINER
            , VP_CLASS_APIBLOCK_CODELINE_ELLIPSIS
            , VP_CLASS_STYLE_DISPLAY_FLEX

            , API_BLOCK_PROCESS_PRODUCTION
            , API_BLOCK_PROCESS_DEVELOPMENT
            , VP_CLASS_APIBLOCK_BUTTONS
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_OPTION_TAB


            , VP_CLASS_STYLE_DISPLAY_BLOCK
            , VP_CLASS_STYLE_DISPLAY_NONE

            , NUM_DELETE_KEY_EVENT_NUMBER
            , NUM_ENTER_KEY_EVENT_NUMBER
            , NUM_APIBLOCK_MAIN_PAGE_WIDTH
            , NUM_APIBLOCK_LEFT_PAGE_WIDTH
            , NUM_OPTION_PAGE_WIDTH
            , NUM_API_BOARD_CENTER_PAGE_WIDTH

            , STR_TOP
            , STR_SCROLL
            , STR_CLICK
            , STR_EMPTY
            , STR_WIDTH 
            , STR_MAX_WIDTH

            , STR_DISPLAY
       
            , STR_BLOCK
            , STR_PARENT
            , STR_NONE
            , STR_NOTEBOOK
            , STR_HEADER
            , STR_CELL
            , STR_CODEMIRROR_LINES

            , STATE_codeLine } = constData;

    const BlockContainer = blockContainer;
    const CreateBlockBtn = createBlockBtn;
    const CreateApiBtn = createApiBtn;
    const CreateGroup = createGroup;
    const { api_listInit 
            , libraryLoadCallback
            , toggleApiListSubGroupShow
            , makeOptionPageNaviInfo
            , loadLibraries
            , loadLibrariesToJson
            , getNavigationInfo } = api_list;

    var init = function(){
        /** 제이쿼리 커스텀 메소드 생성
         *  싱글 클릭 혹은 더블 클릭 바인딩
         * 
         *  이 메소드 하나로 싱글 클릭과 더블 클릭을 동시에 처리할 수 있음
         */
        $.fn.single_double_click = function(single_click_callback, double_click_callback, timeout) {
            return this.each(function(){
                var clicks = 0, 
                    self = this;
                $(this).click(function(event){
                    clicks++;
                    if (clicks == 1) {
                        setTimeout(function(){
                            if(clicks == 1) {
                                single_click_callback.call(self, event);
                            } else {
                                double_click_callback.call(self, event);
                            }
                            clicks = 0;
                        }, timeout || 300);
                    }
                });
            });
        }

        /** block container 생성
         * 싱글톤 무조건 1개
         */
        var blockContainer = new BlockContainer();

        /** Logic에 블럭 그룹 생성 */
        var createLogicGroupArray = Object.values(BLOCK_GROUP_TYPE);
        var logicBlockContainer = VP_CLASS_PREFIX + VP_CLASS_BLOCK_GROUPBOX_PREFIX + 'logic';
        createLogicGroupArray.forEach(enumData => {
            new CreateGroup(blockContainer, enumData, MapGroupTypeToName(enumData), logicBlockContainer);
        });

        /** Logic(Define, Control, Execute)에 블럭 생성 버튼 생성 */
        var createBlockBtnArray = Object.values(BLOCK_CODELINE_BTN_TYPE);
        createBlockBtnArray.forEach(enumData => {
            new CreateBlockBtn(blockContainer, enumData);
        });

        /** 추가: API 버튼 추가 */
        var xmlLibraries = {};
        loadLibrariesToJson(function(param) {
            xmlLibraries = param.getJson();
            // make group & list
            apiLibariesToBtn(blockContainer, xmlLibraries.library);
            
        }, xmlLibraries);

        /** 추가: FIXME: Data Analysis 메뉴 임시 추가 */
        var TEMP_DA_MENUS = [
            'Data Preprocessing',
            'Data Exploration',
            'Visualization',
            'DataBase',
            'Crawling',
            'Machine Learning',
            'Deep Learning'
        ];
        TEMP_DA_MENUS.forEach((menu, idx) => {
            new CreateGroup(blockContainer, 'da_' + idx, menu, VP_CLASS_PREFIX + 'vp-block-group-box-da');
        });

        /** API Block 햄버거 메뉴바 생성 */
        apiBlockMenuInit(blockContainer);

        /** ------------------처음 파일을 오픈할 때 화면의 width 값 계산 ----------------------------------- */
        /** 전체 visual python width 계산 */
        var mainPageRectWidth = $(VP_ID_PREFIX + VP_ID_WRAPPER).css(STR_WIDTH);
        var index = mainPageRectWidth.indexOf('px');
        var mainPageRectWidthNum = parseInt(mainPageRectWidth.slice(0,index));

        /** 왼쪽 Logic, API 블럭 생성 영역의 width*/
        var buttonsPageRectWidth = NUM_APIBLOCK_LEFT_PAGE_WIDTH; 
        /** 가운데 board 영역의 width */
        var boardPageRectWidth = NUM_API_BOARD_CENTER_PAGE_WIDTH;
        // blockContainer.resizeAPIblock();
        /** 오른쪽 option 영역의 width 계산 */
        var optionPageRectWidth = mainPageRectWidthNum - buttonsPageRectWidth - boardPageRectWidth - 103;

        blockContainer.setOptionPageWidth(optionPageRectWidth); 

        $(vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_WRAPPER)).css(STR_WIDTH, mainPageRectWidth);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, optionPageRectWidth);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD_CONTAINER)).css(STR_WIDTH, boardPageRectWidth);
        var optionPageRectWidth_maxWidth = mainPageRectWidthNum - buttonsPageRectWidth - 290 - 103;
        // console.log('optionPageRectWidth',optionPageRectWidth);
        // console.log('mainPageRectWidth',mainPageRectWidth);
        // console.log('optionPageRectWidth_maxWidth',optionPageRectWidth_maxWidth);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_MAX_WIDTH, optionPageRectWidth_maxWidth);

        $(VP_ID_PREFIX + VP_ID_APIBLOCK_BOARD_MAKE_NODE_BLOCK_INPUT).val('Untitled');
        $(VP_ID_PREFIX + VP_ID_APIBLOCK_BOARD_MAKE_NODE_BLOCK_INPUT).focus();

        /** API List xml 데이터를 xmlLibraries에 대입 변수 */
        var xmlLibraries = loadLibraries(VP_ID_PREFIX + VP_ID_APIBLOCK_LEFT_TAB_API);

        /** 블럭이 생성되어 보여지는 container를 생성하고
         *  board에 container dom을 렌더링
         */
        blockContainer.reNewContainerDom();
        
        /** delete 키를 누르거나,
         *  enter키를 누를 때 keyup 이벤트 발동
         */
        $(document).keyup(function(e) {
            var keycode =  e.keyCode 
                                ? e.keyCode 
                                : e.which;

            var selectedBlock = blockContainer.getSelectBlock();

            /** Delete 이벤트 */
            /** block을 클릭하고 delete 키 눌렀을 때 */ 
            if (keycode == NUM_DELETE_KEY_EVENT_NUMBER
                && selectedBlock){

                selectedBlock.deleteBlock_childBlockList();

                blockContainer.resetOptionPage();
                blockContainer.reRenderAllBlock_asc();
            } 

            /** Enter 이벤트 */
            /** 'Untitled이라고 표시된 input 태그에 focus한 상태에서
             *  엔터키를 누르면
             *  input 태그에 적힌 title이름으로 node 블럭 생성
             */
            // if ($(VP_ID_PREFIX + VP_ID_APIBLOCK_BOARD_MAKE_NODE_BLOCK_INPUT).is(":focus") 
                // && window.event.keyCode == NUM_ENTER_KEY_EVENT_NUMBER) {
                // var inputNodeBlockTitleName = $(VP_ID_PREFIX + VP_ID_APIBLOCK_BOARD_MAKE_NODE_BLOCK_INPUT).val();
                // if (inputNodeBlockTitleName == STR_EMPTY) {
                    // vpCommon.renderAlertModal('Required input!');
                    // $(VP_ID_PREFIX + VP_ID_APIBLOCK_BOARD_MAKE_NODE_BLOCK_INPUT).val(STR_EMPTY);
                    // return;
                // }

                // blockContainer.createNodeBlock(true, inputNodeBlockTitleName);
            
                /** node 블럭 생성 했으면
                 *  input 태그 초기화 */
                // $(VP_ID_PREFIX + VP_ID_APIBLOCK_BOARD_MAKE_NODE_BLOCK_INPUT).val(STR_EMPTY);
            // }

        });

        $(document).on(STR_CLICK,`.vp-apiblock-panel-area-vertical-btn`, function(){
            if ($(this).hasClass(`vp-apiblock-arrow-down`)) {
                // 펼치기
                $(this).removeClass(`vp-apiblock-arrow-down`);
                $(this).addClass(`vp-apiblock-arrow-up`);
                $(this).parent().parent().removeClass(`vp-apiblock-minimize`);
            } else {
                // 닫기
                $(this).removeClass(`vp-apiblock-arrow-up`);
                $(this).addClass(`vp-apiblock-arrow-down`);
                $(this).parent().parent().addClass(`vp-apiblock-minimize`);
            }
        });
         
        $(document).on(STR_CLICK,`.vp-block-blocktab-name`, function(){
            var $arrowBtn = $(this).prev();
            if ($($arrowBtn).hasClass(`vp-apiblock-arrow-down`)) {
                // 펼치기
                $($arrowBtn).removeClass(`vp-apiblock-arrow-down`);
                $($arrowBtn).addClass(`vp-apiblock-arrow-up`);
                $($arrowBtn).parent().parent().removeClass(`vp-apiblock-minimize`);
            } else {
                // 닫기
                $($arrowBtn).removeClass(`vp-apiblock-arrow-up`);
                $($arrowBtn).addClass(`vp-apiblock-arrow-down`);
                $($arrowBtn).parent().parent().addClass(`vp-apiblock-minimize`);
            }
        });

        // 추가 : 대메뉴 접기/펼치기
        $('.vp-apiblock-category').on(STR_CLICK, function() {
            var category = $(this).attr('data-category');
            // 해당 대메뉴 접기/펼치기 토글
            $('.vp-block-group-box-' + category).toggle();
        });

        const blockTab_api = $(VP_ID_PREFIX + VP_ID_APIBLOCK_LEFT_TAB_API);
        $(blockTab_api).addClass(VP_CLASS_STYLE_DISPLAY_BLOCK);

        /** api block 화면 이외에 화면을 클릭했을 때, page 포커스 해제 */
        $(vpCommon.wrapSelector(`${VP_ID_PREFIX}${STR_NOTEBOOK}, 
                                ${VP_ID_PREFIX}${STR_HEADER}, 
                                ${VP_CLASS_PREFIX}${STR_CELL}, 
                                ${VP_CLASS_PREFIX}${STR_CODEMIRROR_LINES},
                                div#notebook`)).click(function(event) {
            blockContainer.resetBlockList();
            blockContainer.resetOptionPage();
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.NULL);
        });
        
        /** Create block buttons page를 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS)).click(function(event) {
            if ($(event.target).attr('id') == undefined) {
                blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.BUTTONS);
            } 
        });

        /** Block Board page를 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).click(function(event) {
            /** Board에서 Board page를 클릭하고 block을 클릭하지 않았을 때 */
            if ($(event.target).attr('class')
                && ($(event.target).attr('class').indexOf('vp-apiblock-board-body') != -1 
                    || $(event.target).attr('class').indexOf('vp-block-container') != -1 ) ) {
                blockContainer.resetBlockList();
                blockContainer.resetOptionPage();
                blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);
            }
        });

        /** Block Board 위 Input 영역을 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_ID_PREFIX + "vp_apiblock_board_main_title")).click(function(event) {
            blockContainer.resetBlockList();
            blockContainer.resetOptionPage();
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.BOARD_TITLE);
        });

        /** API List를 클릭했을 때*/
        $(vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_LEFT_TAP_APILIST_PAGE)).click(function(event) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.API_LIST_TAB);
        });

        /** Option page를 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).click(function(event) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.OPTION);
        });
        
        /** 블럭 복사하고 붙여넣는 기능 이벤트 바인딩 */
        $(document).ready(function() {
            var ctrlDown = false,
                ctrlKey = 17,
                cmdKey = 91,
                vKey = 86,
                cKey = 67;
        
            $(document).keydown(function(e) {
                if (e.keyCode == ctrlKey || e.keyCode == cmdKey) {
                    ctrlDown = true;
                }
            }).keyup(function(e) {
                if (e.keyCode == ctrlKey || e.keyCode == cmdKey) {
                    ctrlDown = false;
                }
            });

            $(document).keydown(function(e) {
                /** board에 선택되지 않은 블럭이거나
                *  TEXT 블럭인 경우에 ctrl + c , ctrl + v 금지
                */
                var selectedBlock = blockContainer.getSelectBlock();
                if (!selectedBlock 
                    || selectedBlock.getBlockType() == BLOCK_CODELINE_TYPE.TEXT
                    || selectedBlock.getBlockType() == BLOCK_CODELINE_TYPE.LAMBDA
                    || selectedBlock.getBlockType() == BLOCK_CODELINE_TYPE.CODE
                    || selectedBlock.getBlockType() == BLOCK_CODELINE_TYPE.PRINT
                    || selectedBlock.getBlockType() == BLOCK_CODELINE_TYPE.BREAK 
                    || selectedBlock.getBlockType() == BLOCK_CODELINE_TYPE.CONTINUE
                    || selectedBlock.getBlockType() == BLOCK_CODELINE_TYPE.PASS ) {
                    return;
                }   
                // console.log('selectedBlock',selectedBlock);

                /** ctrl + c */
                if (ctrlDown && (e.keyCode == cKey)) {
                    blockContainer.setCtrlSaveData();
                }

                /** ctrl + v */
                if (ctrlDown && (e.keyCode == vKey)) {

                    const { lastBlock, lastCopyBlocklist_cloned } = blockContainer.getCtrlSaveData();
                    lastBlock.appendBlock(lastCopyBlocklist_cloned, BLOCK_DIRECTION.DOWN);
                    
                    blockContainer.reRenderAllBlock_metadata();
                    blockContainer.setCtrlSaveData();

                    vpCommon.renderSuccessMessage('Blocks copy success!');
                }
            });
        });

        /** node 블럭 생성 버튼 클릭 함수 바인딩 */
        $(document).on(STR_CLICK, VP_ID_PREFIX + VP_ID_APIBLOCK_NODE_BLOCK_PLUS_BUTTON, function() {
            blockContainer.createNodeBlock(true);
        });

        /** text 블럭 생성 버튼 클릭 함수 바인딩 */
        $(document).on(STR_CLICK, VP_ID_PREFIX + VP_ID_APIBLOCK_TEXT_BLOCK_PLUS_BUTTON, function() {
            blockContainer.createTextBlock();
        });

        /**
         * API List item 클릭 이벤트 함수 바인딩
         * API List 목록의 함수에 대응되는 API List 블럭을 생성하기 위해서
         */ 
        $(document).off(STR_CLICK,VP_CLASS_PREFIX + vpConst.LIST_ITEM_LIBRARY + 'li');
        $(document).on(STR_CLICK, VP_CLASS_PREFIX + vpConst.LIST_ITEM_LIBRARY + 'li', function(event) {
            event.stopPropagation();
            if ($(this).hasClass(vpConst.LIST_ITEM_LIBRARY_GROUP)) {
                toggleApiListSubGroupShow($(this));
            } else if ($(this).hasClass(vpConst.LIST_ITEM_LIBRARY_FUNCTION)) {
                const funcID = $(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, ""));
                var naviInfo = getNavigationInfo(funcID);

                /** board에 선택한 API List 블럭 생성 */
                blockContainer.createAPIListBlock(funcID, naviInfo);
            }
        });


        /** API Block의 option을 화면 좌우로 resize하는 이벤트 함수 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).resizable({
            containment: STR_PARENT, // 부모 dom을 기준으로 resize -> 확실하진 않지만 'parent'라고 되어있어서 추정
            handles: 'w', // 'w'는 width 좌우  'h'는 상하 height
            resizeHeight: false // height resize 금지
            // resize 할 경우 계속 실행
            ,resize:(function() {
                blockContainer.setIsOptionPageResize(true);
                blockContainer.resizeOptionPopup();
            })
            // resize 끝나면 멈춤
            ,stop: function(event, ui) { 
                blockContainer.setIsOptionPageResize(false);
            }
        });

        ControlToggleInput();
        return blockContainer;
    }

    var apiLibariesToBtn = function(blockContainer, libObj, parentId = '') {
        if (libObj._type == undefined // root
            || libObj._type == 'package') {
            // 패키지인 경우 그룹 생성
            if (libObj._name != undefined) {
                if (libObj._level == 0) {
                    new CreateGroup(blockContainer, libObj._id, libObj._name, VP_CLASS_PREFIX + 'vp-block-group-box-api', libObj._level);
                } else {
                    new CreateGroup(blockContainer, libObj._id, libObj._name, VP_CLASS_PREFIX + 'vp-apiblock-left-tab-' + parentId, libObj._level);
                }
            }
            // 하위 아이템 있으면 다시 호출
            if (libObj.item) {
                if (typeof libObj.item == "object") {
                    if (Array.isArray(libObj.item)) {
                        // item이 array일 경우
                        libObj.item.forEach(obj => {
                            apiLibariesToBtn(blockContainer, obj, libObj._id);
                        });
                    } else {
                        // 단일 항목일 경우
                        apiLibariesToBtn(blockContainer, libObj.item, libObj._id);
                    }
                }
            }
        } else if (libObj._type == 'function' && libObj.level != "0") {
            // 함수인 경우 버튼 생성 (단, level은 0 이상)
            // parentId 없는 경우 생성안함
            if (parentId != undefined && parentId !== STR_EMPTY) {
                new CreateApiBtn(blockContainer, libObj._id, libObj._name, parentId);
            }
        }
    }

    return init;
});
