var model = null;

function select_model(my_model) {
    $("#graph").html('');
    $.getJSON('{{ request.script_root }}/model/' + my_model, function(data) {
        model = my_model;
        $('#model_id').html(my_model);
        $('#model_name').html(data.name);
        if(data.description != null){
            $('#model_description').html(data.description);
        }
        else{
            $('#model_description').html("{{ _('Não há descrição disponível.') }}");
        }
        $('#model_img').attr('src', data.img);
        if(data.form != null){
            $('#additional_form').html(data.form);
        }
        else{
            $('#additional_form').html("{{ _('Este processo não possui parâmetros.') }}");
        }
        $('#selected_model').show();
        $('#what').val('1');
    });
}

$(document).ready(function() {
    $("#t_method").change(function(){
        if($(this).val() == "0"){
            $("#pid_parameters").show();
            $("#what").val('2');
            $("#what").attr("disabled", true);
        }
        else{
            $("#pid_parameters").hide();
            $("#what").val('1');
            $("#what").attr("disabled", false);
        }
    });
    $("#options").validate({
        onsubmit: true,
        onfocusout: false,
        onkeyup: false,
        onclick: false,
        submitHandler: function(form) {
            // Validation to save resources :P
            if(($("#total").val() / $("#sample").val()) > 5000){
                window.alert(
                    "{{ _('Erro') }}: \n\n{{ _('Seu gráfico teria mais de 5000 pontos.') }}\n" + 
                    "{{ _('Por favor, diminua o Tempo Total ou aumente o Tempo de Amostragem.') }}"
                );
                return false;
            }
            // Wow, we have a model to plot! :D
            ts = Math.round(new Date().getTime() / 1000);
            img_url = '{{ request.script_root }}/plot/' + model + '?' + $("#options").serialize();
            $('#graph').html('<img src="' + img_url + '&uts=' + ts + '" />');
            return false;
        },
        showErrors: function(errorMap, errorList) {
            if(errorList.length > 0) {
                // Dammit!
                var aux = "{{ _('Erros') }}:\n\n";
                for(key in errorMap) {
                    aux += key + ": " + errorMap[key] + "\n";
                }
                window.alert(aux);
            }
        }
    });
});
