<?php
    session_start();
    if(isset($_SESSION["hospital_id"])){
        include_once('config.php');
        $hospt_id = $_SESSION["hospital_id"];
        $query = "SELECT * FROM `hospital` WHERE `HOSPITAL_ID` = $hospt_id";    
        $data = query($query, true, false);
        
        if($data){
            $hospt_name = $data["HOSPITAL_NAME"];
        }
    }
    else{
         echo("<script>location.replace('index.html');</script>"); 
    }
    $pet_id = $_GET['pet'];
?>

<!DOCTYPE HTML>
<html>

    <head>
        <meta charset="utf-8">
        <link href="main.css" rel="stylesheet">
    </head>

    <body>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        <script src="transform.js"></script>
        <script>
            var diagnosises;
            $(document).ready(function() { 
                $.ajax({
                    url : 'load_personal.php',
                    success : function(data){
//                        console.log(JSON.stringify(data));
                        for(key in transform(data)){
//                            console.log('#'+key.toLowerCase());
//                            console.log(data[key]);
                            $('#'+key.toLowerCase()).html(data[key]);
                        }
                        $.ajax({
                           url : 'load_diagnosis.php',
                            success : function(data){
                                diagnosises = data;
                                for(var i=0;i<data.length;i++){
                                    var html = "<div class='content-prev' data-item='"+i+"'>"+data[i].DIAGN_DATE.split(" ")[0]+"</div>";
                                    $('#cell-prev').append(html);
                                    
                                }
                            },
                            type : 'post',
                            dataType: 'json',
                            data : {pet_id : "<?=$pet_id?>", hospt_id : "<?=$hospt_id?>"}
                        });
                            
                    },
                    fail : function(){
                        alert("asdfasdfasdf");
                    },
                    type : 'post',
                    dataType: 'json', 
                    data : {pet_id : "<?=$pet_id ?>"}
                });
            
            });
            
            $(document).on('click','.content-prev',function(){
                $( ".content-prev" ).removeClass('selected');
                $(this).addClass('selected');
                $('#cell-prev-c').html(diagnosises[$(this).attr("data-item")].DIAGN_OPINION);
                
                
                
            });
        </script>
        <div class="navBar">
            <div class="navHeader">
                <div class="hosptName"><?=$hospt_name ?></div>
                <div class="menuHospt">병원관리</div>
            </div>
            <div class="navMenu">
                <ul>
                    <li class="act">기본진료</li>
                    <li>정밀검사</li>
                    <li>마약관리</li>
                    <li>수가/메모</li>
                    <li>보호자관리</li>
                    <li class="chat"><img src="img/chatting%20btn.png" width="90    px" height="90x"></li>
                </ul>
            </div>
        </div>
        <div class="container">
            <div class="row-1">
                <div class="cell personal">
                    <div class="title title-small">개인정보</div>
                    <div class="content-row-1">
                        <div class="title content-cell-1">이&nbsp; &nbsp; &nbsp; 름</div>
                        <div class="content-cell-1" id="pet_name"></div>
                        <div class="title content-cell-1">보 호 자</div>
                        <div class="content-cell-1" id="pet_person"></div>
                    </div>
                    <div class="content-row-1">
                        <div class="title content-cell-1">품&nbsp; &nbsp; &nbsp; 종</div>
                        <div class="content-cell-3" id="pet_spec"></div>
                    </div>
                    <div class="content-row-1">
                        <div class="title content-cell-1">나&nbsp; &nbsp; &nbsp; 이</div>
                        <div class="content-cell-1" id="pet_age"></div>
                        <div class="title content-cell-1">입원여부</div>
                        <div class="content-cell-1" id="pet_adms"></div>
                    </div>
                    <div class="content-row-1">
                        <div class="title content-cell-1">성&nbsp; &nbsp; &nbsp; 별</div>
                        <div class="content-cell-1" id="pet_sex"></div>
                        <div class="title content-cell-1">체&nbsp; &nbsp; &nbsp; 중</div>
                        <div class="content-cell-1" id="pet_weight"></div>
                    </div>
                    <div class="content-row-1">
                        <div class="title content-cell-1">연 락 처</div>
                        <div class="content-cell-3" id="pet_contact"></div>
                    </div>
                    <div class="content-row-2">
                        <div class="title content-cell-1">특이사항</div>
                        <div class="content-cell-3" id="pet_profile"></div>
                    </div>
                </div>
                <div class="cell prev">
                    <div class="title title-small">이전진료</div>
                    
                    <div class="content-cell-prev-c" id="cell-prev-c"></div>
                    <div class="content-cell-prev" id="cell-prev">
                    </div>
                </div>
                <div class="cell now">
                    <div class="title title-small">현재진료</div>
                    <textarea rows="4" style="resize:none;" class="diagnosis"></textarea>
                    
                </div>
        
            </div>
        </div>
        <div class="container">
            <div class="row-2">
                <div class="cell detail">
                    <div class="title title-search">
                        <div class="select">질 병</div>
                        <div class="search"><input type="text"/></div>
                    </div>
                    
                    <div class="search-container">
                        <div class="search-content">
                            <div class="result"></div>
                            <div class="result"></div>
                        </div>
                        <div class="medicine">
                            <div class="title title-small">의약품선택</div>
                        </div>
                    </div>
                    <div class="container medicine-last">
                        <div class="row-3">
                            <div class="cell self">
                                <div class="title title-small">자가관리</div>
                            </div>
                            <div class="cell presc">
                                <div class="title title-small">처방관리</div>
                            </div>
                            <div class="cell price">
                                <div class="title title-small">수가입력</div>
                            </div>

                        </div>

                    
                    </div>
                </div>
                <div class="cell last">
                    <div class="title title-big">종합소견</div>
                    <textarea rows="4" style="resize:none;" class="opinion">나트륨이 과다한 음식은 잦은 소변과 심혈관계 질환을 유발할 수 있으니 피해주세요. 한 주에 30분 이상의 운동을 추천합니다. 정기적인 관리를 하지 않으면 쿠싱과 저혈당 쇼크등의 합병증이 유발될 수 있으니 유의해주세요.</textarea>
                    <div class="total-container">
                        <div class="total-content" style="float:left;">합 계</div>
                        <div class="total-content" style="float:right;">110,200 &#8361;</div>
                    </div>
                    <div class="submit-container">
                        <div class="check">검사하기</div>
                        <div class="submit">처방하기</div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>