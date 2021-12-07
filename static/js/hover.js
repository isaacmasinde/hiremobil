        $(".top").mouseover(function () {
          var id = $(this).attr('span');
          var me= $(this).attr('id');
          document.getElementById(id).style.color='orange';
          document.getElementById(me).style.shadow='2px 2px';
        });

      $(".top").mouseout(function () {
        var id = $(this).attr('span');
        var me= $(this).attr('id');
        document.getElementById(id).style.color='black';
        });