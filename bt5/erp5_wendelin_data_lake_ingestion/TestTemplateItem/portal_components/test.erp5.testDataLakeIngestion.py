from Products.ERP5Type.tests.SecurityTestCase import SecurityTestCase
from pprint import pformat
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from Products.ERP5Type import Permissions
from zExceptions import Unauthorized
import string
import random
import csv
import os
import time
import numpy as np
import base64

class TestDataIngestion(SecurityTestCase):

  REFERENCE_SEPARATOR = "/"
  PART_1 = REFERENCE_SEPARATOR + "001"
  PART_2 = REFERENCE_SEPARATOR + "002"
  PART_3 = REFERENCE_SEPARATOR + "003"
  EOF = REFERENCE_SEPARATOR + "EOF"
  FIF = REFERENCE_SEPARATOR + "fif"
  CSV = REFERENCE_SEPARATOR + "csv"
  SIZE_HASH = REFERENCE_SEPARATOR + "fake-size"+ REFERENCE_SEPARATOR + "fake-hash"
  SINGLE_INGESTION_END = REFERENCE_SEPARATOR
  CHUNK_SIZE_CSV = 25
  REF_PREFIX = "fake-supplier" + REFERENCE_SEPARATOR
  REF_SUPPLIER_PREFIX = "fake-supplier" + REFERENCE_SEPARATOR
  INVALID = "_invalid"
  DOWNLOADER_USER_ID = 'test_downloader'
  CONTRIBUTOR_USER_ID = 'test_contributor'

  def getTitle(self):
    return "DataIngestionTest"

  def afterSetUp(self):
    self.assertEqual(self.REFERENCE_SEPARATOR, self.portal.ERP5Site_getIngestionReferenceDictionary()["reference_separator"])
    self.assertEqual(self.INVALID, self.portal.ERP5Site_getIngestionReferenceDictionary()["invalid_suffix"])
    self.assertEqual(self.EOF, self.REFERENCE_SEPARATOR + self.portal.ERP5Site_getIngestionReferenceDictionary()["split_end_suffix"])
    self.assertEqual(self.PART_1, self.REFERENCE_SEPARATOR + self.portal.ERP5Site_getIngestionReferenceDictionary()["split_first_suffix"])

  def getRandomReference(self):
    random_string = ''.join([random.choice(string.ascii_letters + string.digits) for _ in xrange(10)])
    return 'UNIT-TEST-' + random_string

  def getIngestionReference(self, reference, extension, randomize_ingestion_reference=False, data_set_reference=False):
    if not data_set_reference:
      data_set_reference = "fake-dataset"
    if not randomize_ingestion_reference:
      # return hard coded which results in one Data Set and multiple Data Streams (in context of test)
      return self.REF_PREFIX + data_set_reference + self.REFERENCE_SEPARATOR + reference + extension
    else:
      # create random one
      random_string = self.getRandomReference()
      return "%s/%s/%s/csv//fake-size/fake-hash" %(random_string, random_string, random_string)

  def sanitizeReference(self, reference):
    ingestion_reference = self.REFERENCE_SEPARATOR.join(reference.split(self.REFERENCE_SEPARATOR)[1:])
    data_stream = self.getDataStream(ingestion_reference)
    ingestion_id = data_stream.getId()
    return ingestion_id, ingestion_reference

  def getFullReference(self, ingestion_reference, size, hash_value):
    return self.REF_SUPPLIER_PREFIX + ingestion_reference + self.REFERENCE_SEPARATOR +  self.REFERENCE_SEPARATOR + str("") +  self.REFERENCE_SEPARATOR + ""

  def chunks(self, l, n):
    for i in xrange(0, len(l), n):
      yield l[i:i+n]

  def getDataIngestion(self, reference):
    data_ingestion = self.portal.portal_catalog.getResultValue(
                    portal_type = 'Data Ingestion',
                    reference = reference)
    return data_ingestion

  def getDataStream(self, reference):
    data_stream = self.portal.portal_catalog.getResultValue(
                    portal_type = 'Data Stream',
                    reference = reference)
    return data_stream

  def getDataStreamChunkList(self, reference):
    data_stream_list = self.portal.portal_catalog(
                        portal_type = 'Data Stream',
                        reference = reference,
                        sort_on=[('creation_date', 'ascending')])
    return data_stream_list

  def ingestRequest(self, reference, eof, data_chunk, ingestion_policy):
    encoded_data_chunk = base64.b64encode(data_chunk)
    request = self.portal.REQUEST
    # only POST for Wendelin allowed
    request.environ["REQUEST_METHOD"] = 'POST'
    reference = reference + eof + self.SIZE_HASH
    self.portal.log("Ingest with reference=%s" %reference)
    request.set('reference', reference)
    request.set('data_chunk', encoded_data_chunk)
    ingestion_policy.ingest()
    self.tic()

  def ingest(self, data_chunk, reference, extension, eof, randomize_ingestion_reference=False, data_set_reference=False):
    ingestion_reference = self.getIngestionReference(reference, extension, randomize_ingestion_reference, data_set_reference)
    # use default ebulk policy
    ingestion_policy = self.portal.portal_ingestion_policies.default_ebulk
    self.ingestRequest(ingestion_reference, eof, data_chunk, ingestion_policy)
    _, ingestion_reference = self.sanitizeReference(ingestion_reference)
    return ingestion_reference

  def stepIngest(self, extension, delimiter, randomize_ingestion_reference=False, data_set_reference=False):
    file_name = "file_name.csv"
    reference = self.getRandomReference()
    array = [[random.random() for i in range(self.CHUNK_SIZE_CSV + 10)] for j in range(self.CHUNK_SIZE_CSV + 10)]
    np.savetxt(file_name, array, delimiter=delimiter)
    chunk = []
    with open(file_name, 'r') as csv_file:
      data_chunk = csv_file.read()
      csv_file.seek(0)
      reader = csv.reader(csv_file, delimiter=delimiter)
      for index, line in enumerate(reader):
        if (index < self.CHUNK_SIZE_CSV):
          chunk.append(line)
        else:
          break
    ingestion_reference = self.ingest(data_chunk, reference, extension, self.SINGLE_INGESTION_END,
                                      randomize_ingestion_reference=randomize_ingestion_reference, data_set_reference=data_set_reference)

    if os.path.exists(file_name):
      os.remove(file_name)

    # test properly ingested
    data_ingestion = self.getDataIngestion(ingestion_reference)
    self.assertNotEqual(None, data_ingestion)

    data_ingestion_line = [x for x in data_ingestion.objectValues() \
                            if x.getReference() == 'out_stream'][0]
    data_set = data_ingestion_line.getAggregateValue(portal_type='Data Set')
    data_stream = data_ingestion_line.getAggregateValue(portal_type='Data Stream')
    self.assertNotEqual(None, data_stream)

    data_stream_data = data_stream.getData()
    self.assertEqual(data_chunk, data_stream_data)

    return data_set, [data_stream]

  def createUserCredentials(self, user_id, category_list):
    module = self.portal.getDefaultModule(portal_type='Credential Request')
    if self.portal.CredentialRequest_checkLoginAvailability(user_id):
      credential_request = module.newContent(
        portal_type = "Credential Request",
        first_name = "test_user",
        last_name = user_id,
        reference = user_id,
        password = "test_password",
        default_email_text = user_id + "@lake_security_test.com"
      )
      self.tic()
      credential_request.setCategoryList(category_list)
      tag = 'set_login_%s' % user_id.encode('hex')
      credential_request.reindexObject(activate_kw={'tag': tag})
      credential_request.submit("Automatic submit")
      self.tic()
      if category_list[0] == 'function/downloader':
        # as credential creates contributor assigments by default, change it for downloader user
        person = self.portal.portal_catalog.getResultValue(
                   portal_type = 'Person',
                   default_email_text = user_id + "@lake_security_test.com")
        if person is not None:
          assignment = self.portal.restrictedTraverse('person_module/%s/1' % person.getId())
          assignment.setFunction(['downloader'])

  def failUnlessUserHavePermissionOnDocument(self, permission_name, username, document):
    sm = getSecurityManager()
    try:
      self.loginByUserName(username)
      user = getSecurityManager().getUser()
      if not user.has_permission(permission_name, document):
        groups = []
        if hasattr(user, 'getGroups'):
          groups = user.getGroups()
        raise AssertionError(
          'User %s does NOT have %s permission on %s %s (user roles: [%s], '
          'roles needed: [%s], existing local roles:\n%s\n'
          'your user groups: [%s])' %
          (username, permission_name, document.getPortalTypeName(),
            document, ', '.join(user.getRolesInContext(document)),
           ', '.join([x['name'] for x in
                      document.rolesOfPermission(permission_name)
                      if x['selected']]),
           pformat(document.get_local_roles()),
           ', '.join(groups)))
    finally:
      setSecurityManager(sm)

  def failUnlessUserCanCreateViewAndValidate(self, user_id, container_portal_type, workflow_transition=None):
    reference_base = ''.join(random.choice(string.digits) for x in range(8))
    self.loginByUserName(user_id)

    new_container = self.portal.getDefaultModule(container_portal_type
                            ).newContent(portal_type=container_portal_type,
                                         title=self.id() + reference_base)

    self.failUnlessUserHavePermissionOnDocument(Permissions.View, user_id, new_container)
    self.failUnlessUserHavePermissionOnDocument(Permissions.ModifyPortalContent, user_id, new_container)

  def test_01_DefaultEbulkIngestion(self):
    """
      Test default ingestion with ebulk too.
    """
    data_set, data_stream_list = self.stepIngest(self.CSV, ",", randomize_ingestion_reference=True)

    # check Data Set and Data Stream is validated
    self.assertEqual('validated', data_set.getValidationState())
    self.assertSameSet(['validated' for x in data_stream_list],
                       [x.getValidationState() for x in data_stream_list])

  def test_02_DefaultSplitIngestion(self):
    """
      Test multiple uploads from ebulk end up in multiple Data Streams
      (in case of large file upload when ebluk by default splits file to 50MBs
      chunks).
    """
    data_chunk_1 = ''.join([random.choice(string.ascii_letters + string.digits) \
                              for _ in xrange(250)])
    data_chunk_2 = ''.join([random.choice(string.ascii_letters + string.digits) \
                              for _ in xrange(250)])
    data_chunk_3 = ''.join([random.choice(string.ascii_letters + string.digits) \
                              for _ in xrange(250)])
    data_chunk_4 = ''.join([random.choice(string.ascii_letters + string.digits) \
                              for _ in xrange(250)])

    reference = self.getRandomReference()

    ingestion_reference = self.ingest(data_chunk_1, reference, self.FIF, self.PART_1)
    time.sleep(1)
    self.tic()

    ingestion_reference = self.ingest(data_chunk_2, reference, self.FIF, self.PART_2)
    time.sleep(1)
    self.tic()

    ingestion_reference = self.ingest(data_chunk_3, reference, self.FIF, self.PART_3)
    time.sleep(1)
    self.tic()

    ingestion_reference = self.ingest(data_chunk_4, reference, self.FIF, self.EOF)
    time.sleep(1)
    self.tic()

    # call explicitly alarm so all 4 Data Streams are validated and published
    self.portal.portal_alarms.wendelin_handle_analysis.Alarm_handleAnalysis()
    self.tic()

    # check resulting Data Streams
    data_stream_list = self.getDataStreamChunkList(ingestion_reference)
    #one data stream per chunk
    self.assertEqual(len(data_stream_list), 4)
    #all data streams are validated
    self.assertSameSet(['validated' for x in data_stream_list],
                       [x.getValidationState() for x in data_stream_list])
    #data streams are linked
    data_stream_1 = data_stream_list[0].getObject()
    data_stream_2 = data_stream_list[1].getObject()
    data_stream_3 = data_stream_list[2].getObject()
    data_stream_4 = data_stream_list[3].getObject()
    # test successor
    self.assertSameSet(data_stream_2.getRecursiveSuccessorValueList(), \
                       [data_stream_3, data_stream_4])
    self.assertSameSet(data_stream_4.getRecursiveSuccessorValueList(), \
                       [])
    # test predecessor
    self.assertSameSet(data_stream_1.getRecursivePredecessorValueList(), \
                       [])
    self.assertSameSet(data_stream_2.getRecursivePredecessorValueList(), \
                       [data_stream_1])
    self.assertSameSet(data_stream_4.getRecursivePredecessorValueList(), \
                       [data_stream_3, data_stream_2, data_stream_1])

  def test_03_DefaultWendelinConfigurationExistency(self):
    """
      Test that nobody accidently removes needed by HowTo's default configurations.
    """
    # test default ebuk ingestion exists
    self.assertNotEqual(None,
           getattr(self.portal.portal_ingestion_policies, "default_ebulk", None))
    self.assertNotEqual(None,
           getattr(self.portal.data_supply_module, "embulk", None))

  def test_04_DatasetAndDatastreamsConsistency(self):
    """
      Test that data set state transition also changes its data streams states
    """
    data_set, data_stream_list = self.stepIngest(self.CSV, ",", randomize_ingestion_reference=True)
    self.tic()

    # check data relation between Data Set and Data Streams work
    self.assertSameSet(data_stream_list, data_set.DataSet_getDataStreamList())

    # check data set and all Data Streams states
    self.assertEqual('validated', data_set.getValidationState())
    self.assertSameSet(['validated' for x in data_stream_list],
                       [x.getValidationState() for x in data_stream_list])

    # publish data set and have all Data Streams publsihed automatically
    data_set.publish()
    self.tic()
    self.assertEqual('published', data_set.getValidationState())
    self.assertSameSet(['published' for x in data_stream_list],
                       [x.getValidationState() for x in data_stream_list])

    # invalidate Data Set should invalidate related Data Streams
    data_set.invalidate()
    self.tic()
    self.assertEqual('invalidated', data_set.getValidationState())
    self.assertSameSet(['invalidated' for x in data_stream_list],
                       [x.getValidationState() for x in data_stream_list])

  def test_05_StateConsistencyAlarm(self):
    """
      Test alarm that checks (and fixes) Data set - Data stream state consistency
    """
    data_set_reference = "consistency-dataset-" + self.getRandomReference()
    data_set, data_stream_list = self.stepIngest(self.CSV, ",",
                                      randomize_ingestion_reference=False, data_set_reference=data_set_reference)
    self.tic()
    first_file_stream = data_stream_list[0]

    # publish Data Set (all Data Streams are published automatically)
    data_set.publish()
    self.tic()

    # ingest new file
    data_set, data_stream_list = self.stepIngest(self.CSV, ",",
                                      randomize_ingestion_reference=False, data_set_reference=data_set_reference)
    self.tic()
    second_file_stream = data_stream_list[0]

    # second ingested file stream is in validated state (inconsistent with whole data set state)
    self.assertEqual(data_set.getValidationState(), 'published')
    self.assertEqual(first_file_stream.getValidationState(), 'published')
    self.assertEqual(second_file_stream.getValidationState(), 'validated')

    # call explicitly alarm to fix the state inconsistency
    self.portal.portal_alarms.wendelin_check_datastream_consistency.Alarm_checkDataStreamStateConsistency()
    self.tic()

    # check states where updated (all published)
    self.assertEqual(data_set.getValidationState(), 'published')
    self.assertEqual(first_file_stream.getValidationState(), 'published')
    self.assertEqual(second_file_stream.getValidationState(), 'published')

  def test_06_DefaultModelSecurityModel(self):
    """
      Test default security model : 'All can download, only contributors can upload.'
    """
    #ingest to generate some documents
    self.login()
    data_set, data_stream_list = self.stepIngest(self.CSV, ",", randomize_ingestion_reference=True)
    self.tic()
    data_stream = data_stream_list[0]
    data_ingestion = self.getDataIngestion(data_stream.getReference())
    checkPermission = self.portal.portal_membership.checkPermission

    #create users
    self.createUserCredentials(self.DOWNLOADER_USER_ID, ['function/downloader'])
    self.createUserCredentials(self.CONTRIBUTOR_USER_ID, ['function/contributor'])

    #anonymous can't access modules or not published data
    self.logout()
    self.assertFalse(checkPermission(Permissions.View, self.portal.data_set_module))
    self.assertFalse(checkPermission(Permissions.View, self.portal.data_stream_module))
    self.assertFalse(checkPermission(Permissions.View, self.portal.data_ingestion_module))
    self.assertFalse(checkPermission(Permissions.View, data_set))
    self.assertFalse(checkPermission(Permissions.View, data_stream))
    self.assertFalse(checkPermission(Permissions.View, data_ingestion))
    #publish dataset
    self.login()
    data_set.publish()
    self.tic()
    #anonymous can access published data set and data stream
    self.logout()
    self.assertTrue(checkPermission(Permissions.View, data_set))
    self.assertTrue(checkPermission(Permissions.View, data_stream))
    #anonymous can't ingest
    try:
      self.stepIngest(self.CSV, ",", randomize_ingestion_reference=True)
      self.tic()
      raise AssertionError("Anonymous user should not be able to ingest")
    except Unauthorized:
      pass

    #users can access data
    for user in [self.DOWNLOADER_USER_ID, self.CONTRIBUTOR_USER_ID]:
      self.failUnlessUserHavePermissionOnDocument(Permissions.View, user, self.portal.data_set_module)
      self.failUnlessUserHavePermissionOnDocument(Permissions.View, user, self.portal.data_stream_module)
      self.failUnlessUserHavePermissionOnDocument(Permissions.View, user, self.portal.data_ingestion_module)
      self.failUnlessUserHavePermissionOnDocument(Permissions.View, user, data_set)
      self.failUnlessUserHavePermissionOnDocument(Permissions.View, user, data_stream)
      self.failUnlessUserHavePermissionOnDocument(Permissions.View, user, data_ingestion)

    #downloader can't ingest
    self.loginByUserName(self.DOWNLOADER_USER_ID)
    try:
      self.stepIngest(self.CSV, ",", randomize_ingestion_reference=True)
      self.tic()
      raise AssertionError("Downloader user should not be able to ingest")
    except Unauthorized:
      pass

    #contributor can ingest
    self.loginByUserName(self.CONTRIBUTOR_USER_ID)
    self.failUnlessUserCanCreateViewAndValidate(self.CONTRIBUTOR_USER_ID, 'Data Ingestion', 'validate_action')
    self.stepIngest(self.CSV, ",", randomize_ingestion_reference=True)
    self.tic()

  # XXX: new test which simulates download / upload of Data Set and increase DS version