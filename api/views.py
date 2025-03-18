from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import BPRecord
from .serializers import BPRecordSerializer
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q  
from django.http import JsonResponse
import google.generativeai as genai

genai.configure(api_key="AIzaSyDtsjkld6Vqv0PWy4oOnoBVi15S9imjL_A ")  


def base(request):
    return render(request,'base.html')

@api_view(['POST'])
def create_bp_record(request):
    if request.method == 'POST':
        serializer = BPRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def delete_record(request, pk):
    if request.user.is_superuser:
        record = get_object_or_404(BPRecord, pk=pk)
        record.delete()
    return redirect('admin_dashboard')


@login_required
def admin_dashboard(request):
    search_query = request.GET.get('search', '')  # Get search query from the GET request
    if search_query:
        # Filter records by patient_id if search query exists
        records = BPRecord.objects.filter(patient_id__icontains=search_query)
    else:
        # Show all records if no search query
        records = BPRecord.objects.all()
    return render(request, 'admin_dashboard.html', {'records': records, 'search_query': search_query})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser and password == "BME@123":
                return redirect('admin_dashboard')
            else:
                return redirect('caretaker_dashboard', patient_id=password)
        else:
            messages.error(request,"*Invalid User or Password ")
            return redirect('login')

    return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect('/')

    
@login_required
def admin_dashboard(request):
    records = BPRecord.objects.all()
    return render(request, 'admin_dashboard.html', {'records': records})

@login_required
def caretaker_dashboard(request, patient_id):
    if request.user.is_authenticated and BPRecord.objects.filter(patient_id=patient_id).exists():
        records = BPRecord.objects.filter(patient_id=patient_id)
        return render(request, 'caretaker_dashboard.html', {'records': records, 'patient_id': patient_id})
    else:
        messages.error(request,"Unauthorized access")
        return redirect('login')

def analyze_patient_data(request):
    if request.method == "GET":
        patient_id = request.GET.get('patientid')
        systolic = request.GET.get('systolic')
        diastolic = request.GET.get('diastolic')
        created_date = request.GET.get('created_date')

        # Data for the Generative AI model
        prompt = f"""
        Patient ID: {patient_id}
        Systolic: {systolic}
        Diastolic: {diastolic}
        Created Date: {created_date}

        Based on the given information, analyze the patient's health condition. Diagnose whether the patient's blood pressure is within a normal range, if there is any risk involved (e.g., high risk, needs attention), and provide predictive analysis.
        ###IMPORTANT :
          -Normal Blood Pressure range is 120/80 mmhg 
        ##Format response :
        Example: 
          Analysis:(Must in bold font)
               The patient's blood pressure is below the normal range for adults, indicating possible hypotension (low blood pressure). This condition warrants attention as it may present potential risks, including dizziness, fainting, and, in severe cases, complications such as organ damage. Further investigation is necessary to determine the underlying cause and assess the level of risk.
               
        Rules:
          - Remove the double asterisks (`**`) around the word "Analysis"
          - Avoid including any unnecessary details in the response.
          - Provide a clear and concise analysis of the patient's condition.
          - Strictly Highlight the Double star **Analysis** to bold font
          - Make a well designed and highlighted with colour(eg: good: green, bad : red for words) //Strictly use this (After that remove the dounle star**)
          - Bold the heading.
          -**Analysis** show this in Bold font (Strictly follow this style in all response)
        """
#Recommendations: The patient should seek immediate medical evaluation for proper diagnosis and management. Following medical guidance, potential lifestyle changes such as increased hydration and dietary adjustments may be advised. It is essential to adhere to any treatment plan recommended by a healthcare professional.
        try:
            # Call to the Generative AI model
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            # Return JSON response to the frontend
            return JsonResponse({"response": response.text if hasattr(response, 'text') else str(response)})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

      

# def analyze_patient_data(request):
#     if request.method == "GET":
#         patient_id = request.GET.get('patientid')
#         systolic = request.GET.get('systolic')
#         diastolic = request.GET.get('diastolic')
#         created_date = request.GET.get('created_date')
#         target_dashboard = request.GET.get('dashboard')  # New parameter to identify the target dashboard

#         # Data for the Generative AI model
#         prompt = f"""
#         Patient ID: {patient_id}
#         Systolic: {systolic}
#         Diastolic: {diastolic}
#         Created Date: {created_date}

#         Based on the given information, analyze the patient's health condition. Diagnose whether the patient's blood pressure is within a normal range, if there is any risk involved (e.g., high risk, needs attention), and provide predictive analysis. Offer recommendations for improvement or maintenance without unnecessary details.
#         ##Format response :
#         Example: 
#                Analysis: The patient's blood pressure is below the normal range for adults, indicating possible hypotension (low blood pressure). This condition warrants attention as it may present potential risks, including dizziness, fainting, and, in severe cases, complications such as organ damage. Further investigation is necessary to determine the underlying cause and assess the level of risk.

#                Recommendations: The patient should seek immediate medical evaluation for proper diagnosis and management. Following medical guidance, potential lifestyle changes such as increased hydration and dietary adjustments may be advised. It is essential to adhere to any treatment plan recommended by a healthcare professional.
#         Rules:
#           - Avoid including any unnecessary details in the response.
#           - Provide a clear and concise analysis of the patient's condition.
#           - Avoid giving any recommendations without a clear understanding of the patient's situation.
#           - Give the analysis and recommendations in a structured and logical manner.
#           - Give the analysis and recommendations in a separate line
#           - Strictly Highlight the Double star **Analysis** to bold font
#         """

#         try:
#             # Call to the Generative AI model
#             model = genai.GenerativeModel("gemini-1.5-flash")
#             response = model.generate_content(prompt)
#             analysis_response = response.text if hasattr(response, 'text') else str(response)

#             # Send response based on the target dashboard
#             if target_dashboard == "admindashboard":
#                 return JsonResponse({"admin_response": analysis_response})
#             elif target_dashboard == "caretakerdashboard":
#                 return JsonResponse({"caretaker_response": analysis_response})
#             else:
#                 return JsonResponse({"error": "Invalid dashboard specified"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Invalid request method"}, status=400)
