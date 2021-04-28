var BASE_URL = 'https://'+document.location.host+'/';
function convertVietnamese(str) {
    str = str.toLowerCase();
//     We can also use this instead of from line 11 to line 17
//     str = str.replace(/\u00E0|\u00E1|\u1EA1|\u1EA3|\u00E3|\u00E2|\u1EA7|\u1EA5|\u1EAD|\u1EA9|\u1EAB|\u0103|\u1EB1|\u1EAF|\u1EB7|\u1EB3|\u1EB5/g, "a");
//     str = str.replace(/\u00E8|\u00E9|\u1EB9|\u1EBB|\u1EBD|\u00EA|\u1EC1|\u1EBF|\u1EC7|\u1EC3|\u1EC5/g, "e");
//     str = str.replace(/\u00EC|\u00ED|\u1ECB|\u1EC9|\u0129/g, "i");
//     str = str.replace(/\u00F2|\u00F3|\u1ECD|\u1ECF|\u00F5|\u00F4|\u1ED3|\u1ED1|\u1ED9|\u1ED5|\u1ED7|\u01A1|\u1EDD|\u1EDB|\u1EE3|\u1EDF|\u1EE1/g, "o");
//     str = str.replace(/\u00F9|\u00FA|\u1EE5|\u1EE7|\u0169|\u01B0|\u1EEB|\u1EE9|\u1EF1|\u1EED|\u1EEF/g, "u");
//     str = str.replace(/\u1EF3|\u00FD|\u1EF5|\u1EF7|\u1EF9/g, "y");
//     str = str.replace(/\u0111/g, "d");
    str = str.replace(/Ă |Ă¡|áº¡|áº£|Ă£|Ă¢|áº§|áº¥|áº­|áº©|áº«|Äƒ|áº±|áº¯|áº·|áº³|áºµ/g, "a");
    str = str.replace(/Ă¨|Ă©|áº¹|áº»|áº½|Ăª|á»|áº¿|á»‡|á»ƒ|á»…/g, "e");
    str = str.replace(/Ă¬|Ă­|á»‹|á»‰|Ä©/g, "i");
    str = str.replace(/Ă²|Ă³|á»|á»|Ăµ|Ă´|á»“|á»‘|á»™|á»•|á»—|Æ¡|á»|á»›|á»£|á»Ÿ|á»¡/g, "o");
    str = str.replace(/Ă¹|Ăº|á»¥|á»§|Å©|Æ°|á»«|á»©|á»±|á»­|á»¯/g, "u");
    str = str.replace(/á»³|Ă½|á»µ|á»·|á»¹/g, "y");
    str = str.replace(/Ä‘/g, "d");
    // Some system encode vietnamese combining accent as individual utf-8 characters
    str = str.replace(/\u0300|\u0301|\u0303|\u0309|\u0323/g, ""); // Huyá»n sáº¯c há»i ngĂ£ náº·ng
    str = str.replace(/\u02C6|\u0306|\u031B/g, ""); // Ă‚, Ă, Ä‚, Æ , Æ¯
    return str;
}
var auth = parseInt(jQuery('meta[name=auth]').attr('content'));
    function checkAuth() {
        if(!isNaN(auth) && auth != 0){
            return true;
        }
        return false;
    }
    jQuery(function() {
    //autocomplete
    jQuery("#inset-autocomplete-input").autocomplete({
        source: BASE_URL + 'tim-kiem',
        minLength: 1,
        // autoFocus: true,
        select: function (event, ui){
            console.log(ui.item);
            if(ui.item.type == 'story'){
                if(ui.item.story_type == '1'){
                    window.location.href = 'https://ngontinh.tangthuvien.vn/doc-truyen/'+ ui.item.url;
                }else {
                    window.location.href = BASE_URL+'doc-truyen/'+ ui.item.url;
                }

            }else if(ui.item.type == 'author'){
                window.location.href = BASE_URL+'tac-gia?author='+ ui.item.id;
            }
        }
    }).keypress(function(e){
        if (e.keyCode === 13){
            event.preventDefault();
            window.location.href = BASE_URL+'ket-qua-tim-kiem?term='+jQuery("#inset-autocomplete-input").val();
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        if(item.type == 'story'){
            if(item.story_type == '1'){
                return jQuery( "<li></li>" ).data( "ui-autocomplete-item", item ).append( "<a href='https://ngontinh.tangthuvien.vn/doc-truyen/"+ item.url+"'>" + item.name + "</a>" ).appendTo( ul );
            }else {
                return jQuery( "<li></li>" ).data( "ui-autocomplete-item", item ).append( "<a href='https://truyen.tangthuvien.vn/doc-truyen/"+ item.url+"'>" + item.name + "</a>" ).appendTo( ul );
            }

        }
        if(item.type == 'author'){
            return jQuery( "<li></li>" ).data( "ui-autocomplete-item", item ).append( "<a href='https://truyen.tangthuvien.vn/tac-gia?author="+ item.id+"'>" + item.name + "</a>" ).appendTo( ul );
        }
        // if(item.type == 'converter'){
        //     return jQuery( "<li></li>" ).data( "ui-autocomplete-item", item ).append( "<a href='https://truyen.tangthuvien.vn/dich-gia/"+ item.url+"'>" + item.name + "</a>" ).appendTo( ul );
        // }
        // For now which just want to show the person.given_name in the list.
    };

});

function likeStory(story_id){
    if(!checkAuth()){
        loginBox();
        return false;
    }
    var url = BASE_URL+'likeStory?story_id='+story_id;
   jQuery('#addLikeBtn').removeClass('active');
   jQuery.ajax({url: url, success: function(result){
           jQuery('#addLikeBtn').addClass(result);
           var number = parseInt(jQuery('.ULtwOOTH-like').text());
           if(jQuery('#addLikeBtn').hasClass('active')){
               jQuery('.ULtwOOTH-like').text(number+1);
           }else {
               jQuery('.ULtwOOTH-like').text(number-1);
           }
        }});
}

function followStory(story_id){
    if(!checkAuth()){
        loginBox();
        return false;
    }
    var url = BASE_URL+'follow-story/'+story_id;
    jQuery.ajax({
        url: url,
        success: function(result){
            if(result == '1'){
                var number = parseInt(jQuery('.ULtwOOTH-follow').text());
                if(jQuery('#addFollowBtn').hasClass('active')){
                    jQuery('#addFollowBtn').removeClass('active');
                    jQuery('.ULtwOOTH-follow').text(number-1);
                }else{
                    jQuery('#addFollowBtn').addClass('active');
                    jQuery('.ULtwOOTH-follow').text(number+1);
                }
            }else {
                alert('Truyá»‡n váº«n chÆ°a vĂ o danh sĂ¡ch theo dĂµi cá»§a báº¡n, vui lĂ²ng thá»­ láº¡i sau Ă­t phĂºt.');
            }
        }
    });
}

function nominateStory(story_id) {
    if(!checkAuth()){
        loginBox();
        return false;
    }
    var my_vote =  parseInt(jQuery('#topVoteBtn').attr('data-vote'));
    if(my_vote >0){
        var quantity = prompt("Nháº­p sá»‘ phiáº¿u cho truyá»‡n nĂ y?", '1');
        if (!quantity) {
            return;
        }
        quantity = ( !isNaN(quantity) && parseInt(quantity) > 0 && Number.isInteger(parseInt(quantity)) ) ? parseInt(quantity) : 1;
        if (quantity > my_vote) {
            if(confirm('Äáº¡o há»¯u chá»‰ cĂ²n' + my_vote + ' phiáº¿u Ä‘á» cá»­, cĂ³ thá»ƒ mua thĂªm trong Cá»­a hĂ ng!')){
                window.location.href = BASE_URL+ 'shop-vat-pham';
            }
        }
        else{
            var url = '/vote-story/'+story_id+'?quantity='+quantity;
            jQuery.ajax({
                url: url,
                success: function(result){
                    var number = parseInt(jQuery('.ULtwOOTH-nomi').text());
                    jQuery('.ULtwOOTH-nomi').text(number+quantity);
                    jQuery('#topVoteBtn').attr('data-vote',my_vote-quantity);
                    alert('ÄĂ£ táº·ng phiáº¿u Ä‘á» cá»­!');
                }
            });
        }
    }else {
        if(confirm("Äáº¡o há»¯u khĂ´ng cĂ²n phiáº¿u Ä‘á» cá»­ nĂ o ná»¯a, cĂ³ thá»ƒ mua thĂªm trong Cá»­a hĂ ng!")){
            window.location.href = BASE_URL+ 'shop-vat-pham';
        }
    }
}

function changeTab(number) {
    jQuery('.nav-wrap ul li').removeClass('act');
    if(number == 1){
        jQuery('#j-bookInfoPage').parent().addClass('act');
        jQuery('.catalog-content-wrap').hide();
        jQuery('.book-content-wrap').show();
    }
    if(number==2){
        jQuery('#j-bookCatalogPage').parent().addClass('act');
        jQuery('.catalog-content-wrap').show();
        jQuery('.book-content-wrap').hide();
    }
}
function changeBox(number) {
    jQuery('.comment-head .lang > span').removeClass('act');
    if(number == 1){
        jQuery('.comment-head .lang > span.j_godiscuss').addClass('act');
        jQuery('#userCommentWrap').hide();
        jQuery('#user-discuss').show();
        jQuery('.sendPost').show();
    }
    if(number==2){
        jQuery('.comment-head .lang > span.j_gocomment').addClass('act');
        jQuery('#userCommentWrap').show();
        jQuery('#user-discuss').hide();
        jQuery('.sendPost').hide();
    }
}
function Loading(page) {
    var url = BASE_URL+'doc-truyen/page/'+jQuery('#story_id_hidden').val()+'?page='+page+'&limit=75&web=1';
    console.log(url)
    jQuery.ajax({url: url, success: function(result){
            jQuery("#max-volume").html(result);
        }});
}

function openChilds(el) {
    var id = jQuery(el).attr('data-id');
    jQuery('#discuss-childs-'+id).removeClass('hidden');
}

function loadMoreComment(el){
    jQuery(el).addClass('hidden');
    jQuery('.go-discuss img').removeClass('hidden');
    var story_id = jQuery(el).attr('data-story');
    var page = parseInt(jQuery(el).attr('data-page')) + 1;
    var url = BASE_URL+ 'them-comment/'+story_id+'?page='+page+'&new_web=1';
    jQuery.ajax({url: url, success: function(result){
            jQuery('#user-discuss .discuss-list > ul').append(result);
            jQuery(el).attr('data-page',page);
            jQuery(el).removeClass('hidden');
            jQuery('.go-discuss img').addClass('hidden');
    }});
}

function loadMoreReview(el){
    jQuery(el).addClass('hidden');
    jQuery('.go-reviews img').removeClass('hidden');
    var story_id = jQuery(el).attr('data-story');
    var page = parseInt(jQuery(el).attr('data-page')) + 1;
    var url = BASE_URL+ 'them-review?page='+page+'&story_id='+story_id;
    jQuery.ajax({url: url, success: function(result){
            jQuery('.comment-list dl').append(result);
            jQuery(el).attr('data-page',page);
            jQuery(el).removeClass('hidden');
            jQuery('.go-reviews img').addClass('hidden');
        }});
}

function readmore(el) {
    var id = jQuery(el).attr('data-id');
    jQuery('.cmt-'+id+' .read-only').addClass('hidden');
    jQuery(el).addClass('hidden');
    jQuery('.cmt-'+id+' .read-all').removeClass('hidden');
}

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}

function sendComment(el) {
    if(!checkAuth()){
        loginBox();
        return false;
    }
    var url = BASE_URL+'postComment';
    var txt = jQuery('#form-comment textarea[name=comment]').val();
    if(txt.length > 5){
        jQuery('#form-comment button.btn-post').addClass('disable');
        jQuery('#form-comment button.btn-post').attr('disabled',true);
        jQuery('#form-comment textarea[name=comment]').val('');
        var img = jQuery('#form-comment .comment-avatar img').attr('src');
        var html = '<li class="cf"><div class="user-photo"><a href="javascript:void(0);">' +
            '<img src="'+img+'" draggable="false"/>' +
            '</a></div>' +
            '<div class="discuss-info">' +
            '<p class="users"><a class="blue" href="javascript:void(0);"><b>'+jQuery(el).attr("data-name")+'</b></a><span class="gray">'+jQuery(el).attr("data-rank")+'</span></p>'+
            '<p class="text"><a class="" href="javascript:void(0);" draggable="false">'+txt+'</a></p>'+
            '<p class="info dib-wrap"><span class="mr20">0 hrs</span><a href="javascript:void(0);" onclick="openChilds(this)" class="info-tab mr20">' +
            '<i class="iconfont">î™²</i>' +
            '<span>0 tráº£ lá»i</span>' +
            ' </a><a href="javascript:;" class="info-tab like-btn">' +
            '<i class="iconfont">î™·</i>' +
            '<span>0</span>' +
            '</a></p>'+
            '</div>'+
            '</li>';
        jQuery('#user-discuss .discuss-list > ul').prepend(html);
        jQuery.ajax({
            url: url,
            data: {
                '_token': jQuery('#form-comment input[name=_token]').val(),
                'story_id': jQuery('#form-comment input[name=story_id]').val(),
                'comment': txt,
                'ajax': 1
            },
            method: 'post',
            success: function (result) {

                jQuery('#form-comment button.btn-post').removeClass('disable');
                jQuery('#form-comment button.btn-post').attr('disabled',false);
                reloadComments(jQuery('#form-comment input[name=story_id]').val());
            }
        });
    }else {
        alert('BĂ¬nh luáº­n tá»‘i thiá»ƒu 10 kĂ½ tá»±!');
    }

}

function reloadComments(story_id) {
    var url = BASE_URL+'them-comment/'+story_id+'?page=0&new_web=1';
    jQuery.ajax({
        url: url,
        success: function (result) {
            jQuery('#user-discuss .discuss-list > ul').html(result);
        }
    });
}

function writeReply(el) {
    if(jQuery(el).attr('data-auth') == '1'){
        var id = jQuery(el).attr('data-parent');
        jQuery('.reply-'+id).removeClass('hidden');
        jQuery(el).hide();
    }else {
        loginBox();
    }
}

function sendReply(el) {
    if(!checkAuth()){
        loginBox();
        return false;
    }
    var id = jQuery(el).attr('data-reply');
    var url = BASE_URL+'postReply';
    var txt = jQuery('#reply-box-'+id+' textarea[name=comment]').val();
    if(txt.length > 5){
        jQuery('#reply-box-'+id+' button.btn-post').addClass('disable');
        jQuery('#reply-box-'+id+' button.btn-post').attr('disabled',true);
        jQuery('#reply-box-'+id+' textarea[name=comment]').val('');
        var img = jQuery('#form-comment .comment-avatar img').attr('src');
        var html = '<li class="cf"><div class="user-photo"><a href="javascript:void(0);">' +
            '<img src="'+img+'" draggable="false"/>' +
            '</a></div>' +
            '<div class="discuss-info">' +
            '<p class="users"><a class="blue" href="javascript:void(0);"><b>'+jQuery(el).attr("data-name")+'</b></a><span class="gray">'+jQuery(el).attr("data-rank")+'</span></p>'+
            '<p class="text"><a class="" href="javascript:void(0);" draggable="false">'+txt+'</a></p>'+
            '<p class="info dib-wrap"><span class="mr20">0 hrs</span>' +
            '<a href="javascript:;" class="info-tab like-btn">' +
            '<i class="iconfont">î™·</i>' +
            '<span>0</span>' +
            '</a></p>'+
            '</div>'+
            '</li>';
        jQuery('#discuss-childs-'+id+' > ul').append(html);
        jQuery.ajax({
            url: url,
            data: {
                '_token': jQuery('#reply-box-'+id+' input[name=_token]').val(),
                'story_id': jQuery('#reply-box-'+id+' input[name=story_id]').val(),
                'comment': txt,
                'id_comment_parent':id,
                'ajax': 1
            },
            method: 'post',
            success: function (result) {
                jQuery('#reply-box-'+id+' button.btn-post').removeClass('disable');
                jQuery('#reply-box-'+id+' button.btn-post').attr('disabled',false);
            }
        });
    }else{
        alert('BĂ¬nh luáº­n tá»‘i thiá»ƒu 10 kĂ½ tá»±!');
    }
}

function likeComment(el) {
    if(!checkAuth()){
        loginBox();
        return false;
    }
    var id = jQuery(el).attr('data-rid');
    var url = BASE_URL+'likeComment?id='+id;
    jQuery.ajax({
        url: url,
        success: function (result) {
            var span = jQuery(el).children('span');
            var number = parseInt(jQuery(span).text());
           if(jQuery(el).hasClass('act')){
               jQuery(el).removeClass('act');
               jQuery(span).text(number-1);
           }else {
               jQuery(el).addClass('act');
               jQuery(span).text(number+1);
           }
        }
    });
}

function openReview() {
    if(!checkAuth()){
        loginBox();
        return false;
    }
    jQuery('.lbf-panel').fadeIn();
    jQuery('.lbf-overlay').show();
}

function closeReviewBox() {
    jQuery('.lbf-panel').hide();
    jQuery('.lbf-overlay').hide();
}

function changeStar(el) {
    var label = jQuery(el).attr('title');
    var number = parseInt(jQuery(el).attr('alt'));
    var on = jQuery('#starBig .star-on').attr('data-value');
    var off = jQuery('#starBig .star-off').attr('data-value');
    jQuery('#hint').text(label);
    jQuery('#starBig input[type=hidden][name=score]').val(number);
    for(var i = 1;i<= 5;i++){
        if(i <= number){
            jQuery('#starBig .star-'+i).attr('src',on);
        }else{
            jQuery('#starBig .star-'+i).attr('src',off);
        }

    }
}

function submitReview(el){
    if(!checkAuth()){
        loginBox();
        return false;
    }
    var star = jQuery('#starBig input[type=hidden][name=score]').val();
    var review  = jQuery('#evaMsgText').val();
    var url = BASE_URL + 'rateStory';
    var data = {
        'star':star,
        'content': review,
        'story_id': jQuery(el).attr('data-rid'),
        '_token': jQuery('#evaluatePopup input[type=hidden][name=_token]').val(),
    };
    jQuery.ajax({
        url: url,
        method:'post',
        data: data,
        success: function(result){
            window.location.reload();
        }
    });
}

function removeComment(id){
    if(confirm('Báº¡n cháº¯c cháº¯n xĂ³a bĂ¬nh luáº­n nĂ y?')) {
        var url = BASE_URL+'remove-comment?comment_id=' + id;
        jQuery.ajax({
            url: url,
            success: function (result) {
                if (result == 1) {
                    jQuery('.cmt-' + id).remove();
                }
            }
        });
    }
}

function  loadingComment(){
    var story_id = jQuery('meta[name=book_detail]').attr('content');
    var url = BASE_URL+'story/comments?story_id='+story_id+'&new_web=1';
    jQuery.ajax({
        url: url,
        method:'get',
        success: function(result){
            jQuery('#user-discuss').html(result);
        }});
}
jQuery(document).ready(function(){
     BASE_URL = 'https://'+document.location.host+'/';
    var path_url = jQuery('meta[name=book_path]').attr('content');
     history.replaceState({},path_url,convertVietnamese(path_url));
    loadingComment();
});