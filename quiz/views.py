from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, AnswerChoice
from .forms import QuestionForm, AnswerChoiceFormSet, AnswerChoiceForm


# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .models import Question, AnswerChoice
from .serializers import QuestionSerializer, AnswerChoiceSerializer
from django.http import HttpResponse


def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, prefix='question')
        formset = AnswerChoiceFormSet(request.POST, prefix='choice')

        if question_form.is_valid() and formset.is_valid():
            question = question_form.save()

            for form in formset:
                if form.is_valid() and form.has_changed():
                    choice = form.save(commit=False)
                    choice.question = question
                    choice.save()

            return redirect('display')

    else:
        question_form = QuestionForm(prefix='question')
        formset = AnswerChoiceFormSet(
            queryset=AnswerChoice.objects.none(), prefix='choice')
        # Set the count of additional empty forms you want to display
        formset.extra = 4

    return render(request, 'quiz/createQuestion.html', {
        'question_form': question_form,
        'formset': formset,
    })


# views.py


def take_test2(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_form.save()
        score = 0
        for question in questions:
            selected_choice_id = request.POST.get(
                f'question_{question.id}', None)
            if selected_choice_id:
                selected_choice = AnswerChoice.objects.get(
                    pk=selected_choice_id)
                if selected_choice.is_correct:
                    score += 1

            total_questions = questions.count()
            percentage_score = (score / total_questions) * 100
            return render(request, 'quiz/testResult.html', {'score': score, 'total_questions': total_questions, 'percentage_score': percentage_score})

    else:
        student_form = StudentForm()

    return render(request, '/quiztakeTest.html', {'questions': questions, 'student_form': student_form})


def take_test(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_choice_id = request.POST.get(
                f'question_{question.id}', None)
            if selected_choice_id:
                selected_choice = AnswerChoice.objects.get(
                    pk=selected_choice_id)
                if selected_choice.is_correct:
                    score += 1

        total_questions = questions.count()
        percentage_score = (score / total_questions) * 100
        return render(request, 'quiz/testResult.html', {'score': score, 'total_questions': total_questions, 'percentage_score': percentage_score})

    return render(request, 'quiz/takeTest.html', {'questions': questions})


"""

def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, prefix='question')
        formset = AnswerChoiceFormSet(request.POST, prefix='choice')

        if question_form.is_valid() and formset.is_valid():
            question = question_form.save()

            for form in formset:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()

                # Check if the current choice is the correct one based on user input
                if choice.is_correct:
                    correct_choice = choice
                    break

            return redirect('display')

    else:
        question_form = QuestionForm()
        formset = AnswerChoiceFormSet(
            queryset=AnswerChoice.objects.none(), prefix='choice')
        formset.extra = 4

    return render(request, 'createQuestion.html', {
        'question_form': question_form,
        'formset': formset,
    })



def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, prefix='question')
        formset = AnswerChoiceFormSet(request.POST, prefix='choice')

        if question_form.is_valid() and formset.is_valid():
            question = question_form.save()

            for form in formset:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()

            return redirect('display')

    else:
        question_form = QuestionForm(prefix='question')
        formset = AnswerChoiceFormSet(prefix='choice')

    return render(request, 'createQuestion.html', {
        'question_form': question_form,
        'formset': formset,
    })
"""


def display_questions(request):
    questions = Question.objects.all()

    return render(request, 'quiz/displayQuestion.html', {
        'questions': questions,
    })


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Question, AnswerChoice
# from .serializers import QuestionSerializer

class QuestionCreateView(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChoiceCreateView(APIView):
    def post(self, request):
        serializer = AnswerChoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestView(APIView):
    def post(self, request):
        # Assuming the request data contains a list of question IDs
        question_ids = request.data.get('question_ids', [])
        questions = Question.objects.filter(id__in=question_ids)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionAPIView(APIView):
    def get(self, request):
        articles = Question.objects.all()
        serializer = QuestionSerializer(articles, many=True)
        return Response(serializer.data)


class QuestionDetails(APIView):
    def get(self, request, id):
        queryset = Question.objects.all()
        article = get_object_or_404(queryset, id=id)
        serializer = QuestionSerializer(article)
        return Response(serializer.data)


class AnswerChoiceAPIView(APIView):
    def get(self, request):
        articles = AnswerChoice.objects.all()
        serializer = AnswerChoiceSerializer(articles, many=True)
        return Response(serializer.data)

"""
class ChoiceDetails(APIView):
    def get(self, request):
        try:
            article = AnswerChoice.objects.filter(question=2)
            serializer = AnswerChoiceSerializer(article, many=True)
            return Response(serializer.data)
        except AnswerChoice.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
"""
class ChoiceDetails(APIView):
    def get(self, request, quest):
        articles = AnswerChoice.objects.filter(question=quest)
        
        if articles.exists():
            serializer = AnswerChoiceSerializer(articles, many=True)
            return Response(serializer.data)
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)




def update_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer_choices = AnswerChoice.objects.filter(question=question)
    # choice_count = len(answer_choices)
    # extra = 0
    # if choice_count < 4:
    #     extra = 4 - choice_count

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        answer_choice_formset = AnswerChoiceFormSet(request.POST, prefix='choices', queryset=answer_choices)

        if question_form.is_valid() and answer_choice_formset.is_valid():
            question_form.save()
            answer_choice_formset.save()
            return redirect('display')
    else:
        question_form = QuestionForm(instance=question)
        answer_choice_formset = AnswerChoiceFormSet(prefix='choices', queryset=answer_choices)
        # Set the count of additional empty forms you want to display
        answer_choice_formset.extra = 0

    context = {
        'question': question,
        'question_form': question_form,
        'answer_choice_formset': answer_choice_formset
    }

    return render(request, 'quiz/updateQuestion.html', context)



class QuestionUpdateView(APIView):
    def put(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerChoiceUpdateView(APIView):
    def put(self, request, choice_id):
        try:
            answer_choice = AnswerChoice.objects.get(id=choice_id)
        except AnswerChoice.DoesNotExist:
            return Response({'error': 'AnswerChoice not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AnswerChoiceSerializer(answer_choice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        answer_choices = AnswerChoice.objects.filter(question=question)

        question_serializer = QuestionSerializer(question, data=request.data)
        answer_choice_serializer = AnswerChoiceSerializer(answer_choices, data=request.data, many=True)

        if question_serializer.is_valid() and answer_choice_serializer.is_valid():
            question_serializer.save()
            answer_choice_serializer.save()
            return Response({'success': True})
        else:
            return Response({'success': False, 'errors': {'question': question_serializer.errors, 'choices': answer_choice_serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)




class QuestionUpdateViews(APIView):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        answer_choices = AnswerChoice.objects.filter(question=question)

        question_serializer = QuestionSerializer(question)
        answer_choice_serializer = AnswerChoiceSerializer(answer_choices, many=True)

        context = {
            'question': question_serializer.data,
            'answer_choices': answer_choice_serializer.data,
        }

        return Response(context)

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        answer_choices = AnswerChoice.objects.filter(question=question)

        question_serializer = QuestionSerializer(question, data=request.data)
        answer_choice_serializer = AnswerChoiceSerializer(answer_choices, data=request.data, many=True)

        if question_serializer.is_valid() and answer_choice_serializer.is_valid():
            question_serializer.save()
            answer_choice_serializer.save()
            return Response({'success': True})
        else:
            errors = {}
            if not question_serializer.is_valid():
                errors['question'] = question_serializer.errors
            if not answer_choice_serializer.is_valid():
                errors['choices'] = answer_choice_serializer.errors
            return Response({'success': False, 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)