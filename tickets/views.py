# from django.shortcuts import render
# from .serializers import TicketSerializer
# from .models import Ticket
# # -----------------drf-------------------------
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status




# # Create your views here.
# @api_view(['POST'])
# def api_add_ticket(request):
#     if request.method =='POST':
#         serializer=TicketSerializer(data=request.data , context={'request':request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data , status=status.HTTP_201_CREATED)
#         return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET'])
# def api_view_ticket(request):
#     if request.method == 'GET':
#         tickets = Ticket.objects.select_related('user','event','tier').all()
#         serializer=TicketSerializer(tickets, many=True , context={'request':request})
#         print(serializer.data)
#         return Response(serializer.data)

# @api_view(['PUT','PATCH'])
# def api_edit_ticket(request,pk):
#     try:
#         tickets = Ticket.objects.get(id=pk)
#     except Ticket.DoesNotExist :
#         return Response({"error":"Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     serializer  = TicketSerializer(tickets , data= request.data , partial=(request.method == 'PATCH')) # poython native list[dict]
#     # print(serializer)
#     # print(serializer.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data , status=status.HTTP_200_OK)
    
#     return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
  
# @api_view(['DELETE'])
# def api_delete_ticket(request,pk):
#     try:
#         tickets = Ticket.objects.get(id=pk)
#     except Ticket.DoesNotExist :
#         return Response({"error":"Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     tickets.delete()
#     return Response({"message":"Ticket ndeleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        
    




