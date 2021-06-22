# Generated by Django 3.2.3 on 2021-06-12 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_rename_products_profile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fullsheet',
            name='select_tickets',
            field=models.CharField(choices=[('1-2-3-4-5-6', '1-2-3-4-5-6'), ('7-8-9-10-11-12', '7-8-9-10-11-12'), ('13-14-15-16-17-18', '13-14-15-16-17-18'), ('19-20-21-22-23-24', '19-20-21-22-23-24'), ('25-26-27-28-29-30', '25-26-27-28-29-30'), ('31-32-33-34-35-36', '31-32-33-34-35-36'), ('37-38-39-40-41-42', '37-38-39-40-41-42'), ('43-44-45-46-47-48', '43-44-45-46-47-48'), ('49-50-51-52-53-54', '49-50-51-52-53-54'), ('55-56-57-58-59-60', '55-56-57-58-59-60'), ('61-62-63-64-65-66', '61-62-63-64-65-66'), ('67-68-69-70-71-72', '67-68-69-70-71-72'), ('73-74-75-76-77-78', '73-74-75-76-77-78'), ('79-80-81-82-83-84', '79-80-81-82-83-84'), ('85-86-87-88-89-90', '85-86-87-88-89-90'), ('91-92-93-94-95-96', '91-92-93-94-95-96'), ('97-98-99-100-101-102', '97-98-99-100-101-102'), ('103-104-105-106-107-108', '103-104-105-106-107-108'), ('109-110-111-112-113-114', '109-110-111-112-113-114'), ('115-116-117-118-119-120', '115-116-117-118-119-120'), ('121-122-123-124-125-126', '121-122-123-124-125-126'), ('127-128-129-130-131-132', '127-128-129-130-131-132'), ('133-134-135-136-137-138', '133-134-135-136-137-138'), ('139-140-141-142-143-144', '139-140-141-142-143-144'), ('145-146-147-148-149-150', '145-146-147-148-149-150'), ('151-152-153-154-155-156', '151-152-153-154-155-156'), ('157-158-159-160-161-162', '157-158-159-160-161-162'), ('163-164-165-166-167-168', '163-164-165-166-167-168'), ('169-170-171-172-173-174', '169-170-171-172-173-174'), ('175-176-177-178-179-180', '175-176-177-178-179-180'), ('181-182-183-184-185-186', '181-182-183-184-185-186'), ('187-188-189-190-191-192', '187-188-189-190-191-192'), ('193-194-195-196-197-198', '193-194-195-196-197-198'), ('199-200-201-202-203-204', '199-200-201-202-203-204'), ('205-206-207-208-209-210', '205-206-207-208-209-210'), ('211-212-213-214-215-216', '211-212-213-214-215-216'), ('217-218-219-220-221-222', '217-218-219-220-221-222'), ('223-224-225-226-227-228', '223-224-225-226-227-228'), ('229-230-231-232-233-234', '229-230-231-232-233-234'), ('235-236-237-238-239-240', '235-236-237-238-239-240'), ('241-242-243-244-245-246', '241-242-243-244-245-246'), ('247-248-249-250-251-252', '247-248-249-250-251-252'), ('253-254-255-256-257-258', '253-254-255-256-257-258'), ('259-260-261-262-263-264', '259-260-261-262-263-264'), ('265-266-267-268-269-270', '265-266-267-268-269-270'), ('271-272-273-274-275-276', '271-272-273-274-275-276'), ('277-278-279-280-281-282', '277-278-279-280-281-282'), ('283-284-285-286-287-288', '283-284-285-286-287-288'), ('289-290-291-292-293-294', '289-290-291-292-293-294'), ('295-296-297-298-299-300', '295-296-297-298-299-300'), ('301-302-303-304-305-306', '301-302-303-304-305-306'), ('307-308-309-310-311-312', '307-308-309-310-311-312'), ('313-314-315-316-317-318', '313-314-315-316-317-318'), ('319-320-321-322-323-324', '319-320-321-322-323-324'), ('325-326-327-328-329-330', '325-326-327-328-329-330'), ('331-332-333-334-335-336', '331-332-333-334-335-336'), ('337-338-339-340-341-342', '337-338-339-340-341-342'), ('343-344-345-346-347-348', '343-344-345-346-347-348'), ('349-350-351-352-353-354', '349-350-351-352-353-354'), ('355-356-357-358-359-360', '355-356-357-358-359-360'), ('361-362-363-364-365-366', '361-362-363-364-365-366'), ('367-368-369-370-371-372', '367-368-369-370-371-372'), ('373-374-375-376-377-378', '373-374-375-376-377-378'), ('379-380-381-382-383-384', '379-380-381-382-383-384'), ('385-386-387-388-389-390', '385-386-387-388-389-390'), ('391-392-393-394-395-396', '391-392-393-394-395-396'), ('397-398-399-400-401-402', '397-398-399-400-401-402'), ('403-404-405-406-407-408', '403-404-405-406-407-408'), ('409-410-411-412-413-414', '409-410-411-412-413-414'), ('415-416-417-418-419-420', '415-416-417-418-419-420'), ('421-422-423-424-425-426', '421-422-423-424-425-426'), ('427-428-429-430-431-432', '427-428-429-430-431-432'), ('433-434-435-436-437-438', '433-434-435-436-437-438'), ('439-440-441-442-443-444', '439-440-441-442-443-444'), ('445-446-447-448-449-450', '445-446-447-448-449-450'), ('451-452-453-454-455-456', '451-452-453-454-455-456'), ('457-458-459-460-461-462', '457-458-459-460-461-462'), ('463-464-465-466-467-468', '463-464-465-466-467-468'), ('469-470-471-472-473-474', '469-470-471-472-473-474'), ('475-476-477-478-479-480', '475-476-477-478-479-480'), ('481-482-483-484-485-486', '481-482-483-484-485-486'), ('487-488-489-490-491-492', '487-488-489-490-491-492'), ('493-494-495-496-497-498', '493-494-495-496-497-498'), ('499-500-501-502-503-504', '499-500-501-502-503-504'), ('505-506-507-508-509-510', '505-506-507-508-509-510'), ('511-512-513-514-515-516', '511-512-513-514-515-516'), ('517-518-519-520-521-522', '517-518-519-520-521-522'), ('523-524-525-526-527-528', '523-524-525-526-527-528'), ('529-530-531-532-533-534', '529-530-531-532-533-534'), ('535-536-537-538-539-540', '535-536-537-538-539-540'), ('541-542-543-544-545-546', '541-542-543-544-545-546'), ('547-548-549-550-551-552', '547-548-549-550-551-552'), ('553-554-555-556-557-558', '553-554-555-556-557-558'), ('559-560-561-562-563-564', '559-560-561-562-563-564'), ('565-566-567-568-569-570', '565-566-567-568-569-570'), ('571-572-573-574-575-576', '571-572-573-574-575-576'), ('577-578-579-580-581-582', '577-578-579-580-581-582'), ('583-584-585-586-587-588', '583-584-585-586-587-588'), ('589-590-591-592-593-594', '589-590-591-592-593-594'), ('595-596-597-598-599-600', '595-596-597-598-599-600')], max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='halfsheet',
            name='select_tickets',
            field=models.CharField(choices=[('1-2-3', '1-2-3'), ('4-5-6', '4-5-6'), ('7-8-9', '7-8-9'), ('10-11-12', '10-11-12'), ('13-14-15', '13-14-15'), ('16-17-18', '16-17-18'), ('19-20-21', '19-20-21'), ('22-23-24', '22-23-24'), ('25-26-27', '25-26-27'), ('28-29-30', '28-29-30'), ('31-32-33', '31-32-33'), ('34-35-36', '34-35-36'), ('37-38-39', '37-38-39'), ('40-41-42', '40-41-42'), ('43-44-45', '43-44-45'), ('46-47-48', '46-47-48'), ('49-50-51', '49-50-51'), ('52-53-54', '52-53-54'), ('55-56-57', '55-56-57'), ('58-59-60', '58-59-60'), ('61-62-63', '61-62-63'), ('64-65-66', '64-65-66'), ('67-68-69', '67-68-69'), ('70-71-72', '70-71-72'), ('73-74-75', '73-74-75'), ('76-77-78', '76-77-78'), ('79-80-81', '79-80-81'), ('82-83-84', '82-83-84'), ('85-86-87', '85-86-87'), ('88-89-90', '88-89-90'), ('91-92-93', '91-92-93'), ('94-95-96', '94-95-96'), ('97-98-99', '97-98-99'), ('100-101-102', '100-101-102'), ('103-104-105', '103-104-105'), ('106-107-108', '106-107-108'), ('109-110-111', '109-110-111'), ('112-113-114', '112-113-114'), ('115-116-117', '115-116-117'), ('118-119-120', '118-119-120'), ('121-122-123', '121-122-123'), ('124-125-126', '124-125-126'), ('127-128-129', '127-128-129'), ('130-131-132', '130-131-132'), ('133-134-135', '133-134-135'), ('136-137-138', '136-137-138'), ('139-140-141', '139-140-141'), ('142-143-144', '142-143-144'), ('145-146-147', '145-146-147'), ('148-149-150', '148-149-150'), ('151-152-153', '151-152-153'), ('154-155-156', '154-155-156'), ('157-158-159', '157-158-159'), ('160-161-162', '160-161-162'), ('163-164-165', '163-164-165'), ('166-167-168', '166-167-168'), ('169-170-171', '169-170-171'), ('172-173-174', '172-173-174'), ('175-176-177', '175-176-177'), ('178-179-180', '178-179-180'), ('181-182-183', '181-182-183'), ('184-185-186', '184-185-186'), ('187-188-189', '187-188-189'), ('190-191-192', '190-191-192'), ('193-194-195', '193-194-195'), ('196-197-198', '196-197-198'), ('199-200-201', '199-200-201'), ('202-203-204', '202-203-204'), ('205-206-207', '205-206-207'), ('208-209-210', '208-209-210'), ('211-212-213', '211-212-213'), ('214-215-216', '214-215-216'), ('217-218-219', '217-218-219'), ('220-221-222', '220-221-222'), ('223-224-225', '223-224-225'), ('226-227-228', '226-227-228'), ('229-230-231', '229-230-231'), ('232-233-234', '232-233-234'), ('235-236-237', '235-236-237'), ('238-239-240', '238-239-240'), ('241-242-243', '241-242-243'), ('244-245-246', '244-245-246'), ('247-248-249', '247-248-249'), ('250-251-252', '250-251-252'), ('253-254-255', '253-254-255'), ('256-257-258', '256-257-258'), ('259-260-261', '259-260-261'), ('262-263-264', '262-263-264'), ('265-266-267', '265-266-267'), ('268-269-270', '268-269-270'), ('271-272-273', '271-272-273'), ('274-275-276', '274-275-276'), ('277-278-279', '277-278-279'), ('280-281-282', '280-281-282'), ('283-284-285', '283-284-285'), ('286-287-288', '286-287-288'), ('289-290-291', '289-290-291'), ('292-293-294', '292-293-294'), ('295-296-297', '295-296-297'), ('298-299-300', '298-299-300'), ('301-302-303', '301-302-303'), ('304-305-306', '304-305-306'), ('307-308-309', '307-308-309'), ('310-311-312', '310-311-312'), ('313-314-315', '313-314-315'), ('316-317-318', '316-317-318'), ('319-320-321', '319-320-321'), ('322-323-324', '322-323-324'), ('325-326-327', '325-326-327'), ('328-329-330', '328-329-330'), ('331-332-333', '331-332-333'), ('334-335-336', '334-335-336'), ('337-338-339', '337-338-339'), ('340-341-342', '340-341-342'), ('343-344-345', '343-344-345'), ('346-347-348', '346-347-348'), ('349-350-351', '349-350-351'), ('352-353-354', '352-353-354'), ('355-356-357', '355-356-357'), ('358-359-360', '358-359-360'), ('361-362-363', '361-362-363'), ('364-365-366', '364-365-366'), ('367-368-369', '367-368-369'), ('370-371-372', '370-371-372'), ('373-374-375', '373-374-375'), ('376-377-378', '376-377-378'), ('379-380-381', '379-380-381'), ('382-383-384', '382-383-384'), ('385-386-387', '385-386-387'), ('388-389-390', '388-389-390'), ('391-392-393', '391-392-393'), ('394-395-396', '394-395-396'), ('397-398-399', '397-398-399'), ('400-401-402', '400-401-402'), ('403-404-405', '403-404-405'), ('406-407-408', '406-407-408'), ('409-410-411', '409-410-411'), ('412-413-414', '412-413-414'), ('415-416-417', '415-416-417'), ('418-419-420', '418-419-420'), ('421-422-423', '421-422-423'), ('424-425-426', '424-425-426'), ('427-428-429', '427-428-429'), ('430-431-432', '430-431-432'), ('433-434-435', '433-434-435'), ('436-437-438', '436-437-438'), ('439-440-441', '439-440-441'), ('442-443-444', '442-443-444'), ('445-446-447', '445-446-447'), ('448-449-450', '448-449-450'), ('451-452-453', '451-452-453'), ('454-455-456', '454-455-456'), ('457-458-459', '457-458-459'), ('460-461-462', '460-461-462'), ('463-464-465', '463-464-465'), ('466-467-468', '466-467-468'), ('469-470-471', '469-470-471'), ('472-473-474', '472-473-474'), ('475-476-477', '475-476-477'), ('478-479-480', '478-479-480'), ('481-482-483', '481-482-483'), ('484-485-486', '484-485-486'), ('487-488-489', '487-488-489'), ('490-491-492', '490-491-492'), ('493-494-495', '493-494-495'), ('496-497-498', '496-497-498'), ('499-500-501', '499-500-501'), ('502-503-504', '502-503-504'), ('505-506-507', '505-506-507'), ('508-509-510', '508-509-510'), ('511-512-513', '511-512-513'), ('514-515-516', '514-515-516'), ('517-518-519', '517-518-519'), ('520-521-522', '520-521-522'), ('523-524-525', '523-524-525'), ('526-527-528', '526-527-528'), ('529-530-531', '529-530-531'), ('532-533-534', '532-533-534'), ('535-536-537', '535-536-537'), ('538-539-540', '538-539-540'), ('541-542-543', '541-542-543'), ('544-545-546', '544-545-546'), ('547-548-549', '547-548-549'), ('550-551-552', '550-551-552'), ('553-554-555', '553-554-555'), ('556-557-558', '556-557-558'), ('559-560-561', '559-560-561'), ('562-563-564', '562-563-564'), ('565-566-567', '565-566-567'), ('568-569-570', '568-569-570'), ('571-572-573', '571-572-573'), ('574-575-576', '574-575-576'), ('577-578-579', '577-578-579'), ('580-581-582', '580-581-582'), ('583-584-585', '583-584-585'), ('586-587-588', '586-587-588'), ('589-590-591', '589-590-591'), ('592-593-594', '592-593-594'), ('595-596-597', '595-596-597'), ('598-599-600', '598-599-600')], max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='User_Type',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Developer', 'Developer'), ('SuperUser', 'SuperUser'), ('Agent', 'Agent')], default='Agent', max_length=20),
        ),
    ]
