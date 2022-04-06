$(document).ready(function() {
//    $('#id_program').hide();
//    $('#id_year').hide();




        $("#id_department").html('<option value="">---------------------</option>{% for x,dept in form.fields.department.choices %}<option {% if initial.department.name == x %}  selected {% endif %} value="{{x}}">{{dept}}</option>{% endfor %}');
        var dept_val = $('#id_department').find(":selected").val();
        if( dept_val == 'IBED'){
            $("#id_program").html('<option value="">---------------------</option>{% for x,prog in form.fields.program.choices|slice:"0:3" %}<option {% if initial.program.name == x %}  selected {% endif %} value="{{x}}">{{prog}}</option>{% endfor %}');
            }
        else{
            $("#id_program").html('<option value="">---------------------</option>{% for x,prog in form.fields.program.choices|slice:"3:14" %}<option {% if initial.program.name == x %}  selected {% endif %} value="{{x}}">{{prog}}</option>{% endfor %}');
        }
        var prog_val = $('#id_program').find(":selected").val();
        var year_val = $('#id_year').find(":selected").val();
        if(prog_val == "Grade"){
            $("#id_year").html('<option value="">---------------------</option>{% for x,yr in form.fields.year.choices|slice:"0:6" %}<option {% if initial.year.name == x %}  selected {% endif %} value="{{x}}">{{yr}}</option>{% endfor %}');
        }
        else if(prog_val == "Junior"){
            $("#id_year").html('<option value="">---------------------</option>{% for x,yr in form.fields.year.choices|slice:"6:10" %}<option {% if initial.year.name == x %}  selected {% endif %} value="{{x}}">{{yr}}</option>{% endfor %}');
        }
        else if(prog_val == "Senior"){
            $("#id_year").html('<option value="">---------------------</option>{% for x,yr in form.fields.year.choices|slice:"10:12" %}<option {% if initial.year.name == x %}  selected {% endif %} value="{{x}}">{{yr}}</option>{% endfor %}');
        }
        else if(prog_val.indexOf("----")>=0){
            $("#id_year").html('<option value="">---------------------</option>');
        }
        else{
            $("#id_year").html('<option value="">---------------------</option>{% for x,yr in form.fields.year.choices|slice:"12:17" %}<option {% if initial.year.name == x %}  selected {% endif %} value="{{x}}">{{yr}}</option>{% endfor %}');
        }

    $('#id_department').change(function(){
        dept_val=this.value;
        if(dept_val=="IBED"){
            $("#id_program").html('<option value="">---------------------</option>{% for x,prog in form.fields.program.choices|slice:"0:3" %}<option value="{{x}}">{{prog}}</option>{% endfor %}');
            $("#id_year").html('<option value="">---------------------</option>');
        }
        else{
            $("#id_program").html('<option value="">---------------------</option>{% for x,prog in form.fields.program.choices|slice:"4:14" %}<option {% if initial.program.name == x %}  selected {% endif %} value="{{x}}">{{prog}}</option>{% endfor %}');
            $("#id_year").html('<option value="">---------------------</option>');
        }
        $('#id_program').show();
    });

    $('#id_program').change(function(){
          prog_val=this.value;
          console.log(prog_val)
        if(this.value=="Grade"){
            $("#id_year").html('<option value="">---------------------</option>{% for x,yr in form.fields.year.choices|slice:"0:6" %}<option {% if initial.year.name == x %}  selected {% endif %} value="{{x}}">{{yr}}</option>{% endfor %}');
        }
        else if(this.value=="Junior"){
            $("#id_year").html('<option value="">---------------------</option>{% for x,yr in form.fields.year.choices|slice:"6:10" %}<option {% if initial.year.name == x %}  selected {% endif %} value="{{x}}">{{yr}}</option>{% endfor %}');
        }
         else if(this.value=="Senior"){
            $("#id_year").html('<option value="">---------------------</option>{% for x,yr in form.fields.year.choices|slice:"10:12" %}<option {% if initial.year.name == x %}  selected {% endif %} value="{{x}}">{{yr}}</option>{% endfor %}');
        }
        else if(!prog_val){
            $("#id_year").html('<option value="">---------------------</option>');
        }
        else{
            $("#id_year").html('<option value="">---------------------</option>{% for x,yr in form.fields.year.choices|slice:"12:17" %}<option {% if initial.year.name == x %}  selected {% endif %} value="{{x}}">{{yr}}</option>{% endfor %}');
        }
        $('#id_year').show();
    });

});